from arduino.app_utils import App
from arduino.app_bricks.streamlit_ui import st

import numpy as np
import time
import cv2
import plotly.express as px

import pyrealsense as rsw

DEPTH_RANGE_M = [0.1, 10.0]

############################################################
# Streamlit UI
############################################################

st.title("UNO Q RealSense Processed Depth Viewer (FAST OpenCV + Plotly)")

############################################################
# Pipeline Controls
############################################################

if st.button("Enable Advanced Mode", key="adv_mode_btn"):
    st.write(rsw.enableAdvancedMode())

preset_name = st.text_input("Preset Name", "d4xx-high-accuracy", key="preset_name")
if st.button("Load Preset", key="load_preset_btn"):
    st.write(rsw.loadPreset(preset_name))

if st.button("Initialize Pipeline", key="init_btn"):
    st.write(rsw.init(align_to="color"))

if st.button("Configure Streams", key="cfg_btn"):
    st.write(rsw.configure(
        depth=(640, 480, 30, "z16"),
        color=(640, 480, 30, "bgr8")
    ))

depth_scale = None

if st.button("Start Pipeline", key="start_btn"):
    st.write(rsw.start())
    depth_scale = rsw.getDepthScale()["depth_scale_m"]
    rsw.enableFilter("decimation", 1)
    rsw.enableFilter("threshold", 1)
    rsw.setFilterThreshold(DEPTH_RANGE_M[0], DEPTH_RANGE_M[1])
    rsw.enableFilter("depth2disparity", 1)
    rsw.enableFilter("spatial", 1)
    rsw.enableFilter("temporal", 1)
    rsw.enableFilter("hole_filling", 0)
    rsw.enableFilter("disparity2depth", 1)

    rsw.applyFilters()
    st.write(f"Depth scale: {depth_scale}")

############################################################
# Visualization Controls
############################################################

colormap_name = st.selectbox(
    "Colormap",
    ["turbo", "jet", "inferno", "magma", "plasma", "viridis", "cividis", "gray"],
    key="colormap_select"
)

min_depth_slider, max_depth_slider = st.slider(
    "Depth Range (meters)",
    0.1, 10.0, (0.2, 4.0),
    key="depth_range_slider"
)

show_hist = st.checkbox("Show Depth Histogram", key="hist_checkbox")
show_color = st.checkbox("Show Color Frame", key="color_checkbox")

############################################################
# Stable layout containers (NO STACKING)
############################################################

col1, col2 = st.columns(2)
color_container = col1.empty()
depth_container = col2.empty()
hist_container = st.empty()
fps_container = st.empty()

############################################################
# Depth Viewer Loop
############################################################

run_stream = st.checkbox("Run Depth Stream", key="run_stream")

# OpenCV colormap mapping
cv2_cmap = {
    "turbo": cv2.COLORMAP_TURBO,
    "jet": cv2.COLORMAP_JET,
    "inferno": cv2.COLORMAP_INFERNO,
    "magma": cv2.COLORMAP_MAGMA,
    "plasma": cv2.COLORMAP_PLASMA,
    "viridis": cv2.COLORMAP_VIRIDIS,
    "cividis": cv2.COLORMAP_CIVIDIS,
    "gray": cv2.COLORMAP_BONE
}

while run_stream:

    t0 = time.time()

    try:
        frame = rsw.getAlignedFrames()

        if not frame or "depth" not in frame:
            fps_container.write("No depth frame")
            time.sleep(0.03)
            continue

        depth = np.array(frame["depth"], dtype=np.uint16)
        color = frame.get("color", None)

        # Convert to meters
        if depth_scale is None:
            depth_scale = rsw.getDepthScale()["depth_scale_m"]

        depth_m = depth * depth_scale

        ############################################################
        # Clip depth using slider (ignore zeros)
        ############################################################

        valid = depth_m[(depth_m > min_depth_slider) & (depth_m < max_depth_slider)]

        if len(valid) > 0:
            min_m = np.percentile(valid, 5)
            max_m = np.percentile(valid, 95)
        else:
            min_m, max_m = min_depth_slider, max_depth_slider

        depth_clipped = np.clip(depth_m, min_m, max_m)

        ############################################################
        # Normalize depth
        ############################################################

        depth_norm = (depth_clipped - min_m) / (max_m - min_m)
        depth_norm = np.nan_to_num(depth_norm)

        # Convert to uint8 for OpenCV
        depth_uint8 = (depth_norm * 255).astype(np.uint8)

        ############################################################
        # FAST OpenCV colormap
        ############################################################

        depth_color = cv2.applyColorMap(depth_uint8, cv2_cmap[colormap_name])
        depth_color = cv2.cvtColor(depth_color, cv2.COLOR_BGR2RGB)

        ############################################################
        # Update containers (NO STACKING)
        ############################################################

        if show_color and color is not None:
            # Convert RealSense BGR → RGB
            color_image = np.array(color, dtype=np.uint8)
            color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        
            color_container.image(color_image,
                                  caption="Color Frame",
                                  use_container_width=True)
        else:
            color_container.write("Color frame hidden")

        depth_container.image(depth_color,
                              caption=f"Depth ({colormap_name})",
                              use_container_width=True)

        ############################################################
        # FAST Plotly histogram
        ############################################################

        if show_hist:
            fig = px.histogram(valid, nbins=100, title="Depth Histogram")
            hist_container.plotly_chart(fig, use_container_width=True)
        else:
            hist_container.empty()

        ############################################################
        # FPS
        ############################################################

        fps = 1.0 / (time.time() - t0)
        fps_container.write(f"FPS: {fps:.1f}")

    except Exception as e:
        fps_container.write(f"Error: {e}")

    time.sleep(0.03)

App.run()
