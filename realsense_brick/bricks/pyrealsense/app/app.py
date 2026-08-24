from flask import Flask, request, jsonify
import pyrealsense2 as rs
import numpy as np

app = Flask(__name__)

pipe = None
profile = None
cfg = None
align = None
depth_intrinsics = None


# Helper
def _get_depth_sensor():
    ctx = rs.context()
    dev = ctx.query_devices()[0]
    return dev.query_sensors()[0]

def _get_color_sensor():
    ctx = rs.context()
    dev = ctx.query_devices()[0]
    return dev.query_sensors()[1]

def _pipeline_running():
    try:
        pipe.get_active_profile()
        return True
    except:
        return False


# ---------------------------------------------------------
# Global RealSense pipeline
# ---------------------------------------------------------

@app.route("/rs/init", methods=["POST"])
def rs_init():
    try:
        global pipe, profile, align

        # Read alignment target from Python
        params = request.json or {}
        align_to = params.get("align_to", "color")

        # Create pipeline
        pipe = rs.pipeline()

        # Create align object
        if align_to == "depth":
            align = rs.align(rs.stream.depth)
        else:
            align = rs.align(rs.stream.color)

        profile = None

        return jsonify({
            "status": "initialized",
            "align_to": align_to
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/rs/configure", methods=["POST"])
def rs_configure():
    try:
        params = request.json

        depth_w = params.get("depth_width", 640)
        depth_h = params.get("depth_height", 480)
        depth_fps = params.get("depth_fps", 30)
        depth_format = params.get("depth_format", "z16")

        color_w = params.get("color_width", 640)
        color_h = params.get("color_height", 480)
        color_fps = params.get("color_fps", 30)
        color_format = params.get("color_format", "bgr8")

        depth_fmt_enum = getattr(rs.format, depth_format)
        color_fmt_enum = getattr(rs.format, color_format)

        global cfg
        cfg = rs.config()

        cfg.enable_stream(rs.stream.depth, depth_w, depth_h, depth_fmt_enum, depth_fps)
        cfg.enable_stream(rs.stream.color, color_w, color_h, color_fmt_enum, color_fps)

        return jsonify({
            "status": "configured",
            "depth": [depth_w, depth_h, depth_fps, depth_format],
            "color": [color_w, color_h, color_fps, color_format]
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

#############################
# enumerate devices
#############################
@app.route("/rs/enumerate")
def rs_enumerate():
    ctx = rs.context()
    try:
        devices = ctx.query_devices()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    out = []
    for dev in devices:
        try:
            info = {
                "name": dev.get_info(rs.camera_info.name),
                "serial_number": dev.get_info(rs.camera_info.serial_number),
                "product_id": dev.get_info(rs.camera_info.product_id),
                "firmware_version": dev.get_info(rs.camera_info.firmware_version),
                "physical_port": dev.get_info(rs.camera_info.physical_port),
            }
            out.append(info)
        except Exception as e:
            out.append({"status": "error", "message": str(e)})

    return jsonify({"devices": out})

# ---------------------------------------------------------
# Start / Stop
# ---------------------------------------------------------

@app.route("/rs/start", methods=["POST"])
def rs_start():
    global pipe, profile, cfg, depth_intrinsics

    profile = pipe.start(cfg)

    # Store REAL intrinsics struct
    depth_stream = profile.get_stream(rs.stream.depth)
    video_profile = depth_stream.as_video_stream_profile()
    depth_intrinsics = video_profile.intrinsics

    return jsonify({"status": "started"})



@app.route("/rs/stop", methods=["POST"])
def rs_stop():
    pipe.stop()
    return jsonify({"status": "stopped"})

# ---------------------------------------------------------
# Status
# ---------------------------------------------------------

@app.route("/rs/status")
def rs_status():
    return jsonify({"status": "pyrealsense2 online"})

# ---------------------------------------------------------
# Depth Scale
# ---------------------------------------------------------

@app.route("/rs/get_depth_scale")
def rs_get_depth_scale():
    depth_sensor = profile.get_device().first_depth_sensor()
    scale = depth_sensor.get_depth_scale()
    return jsonify({"depth_scale_m": scale})

# ---------------------------------------------------------
# Intrinsics
# ---------------------------------------------------------

@app.route("/rs/intrinsics")
def rs_intrinsics():
    depth_stream = profile.get_stream(rs.stream.depth)
    intr = depth_stream.as_video_stream_profile().get_intrinsics()

    return jsonify({
        "width": intr.width,
        "height": intr.height,
        "fx": intr.fx,
        "fy": intr.fy,
        "ppx": intr.ppx,
        "ppy": intr.ppy,
        "model": str(intr.model),
        "coeffs": intr.coeffs
    })

# ---------------------------------------------------------
# Extrinsics
# ---------------------------------------------------------

@app.route("/rs/extrinsics")
def rs_extrinsics():
    depth_stream = profile.get_stream(rs.stream.depth)
    color_stream = profile.get_stream(rs.stream.color)
    extr = depth_stream.get_extrinsics_to(color_stream)

    return jsonify({
        "rotation": extr.rotation,
        "translation": extr.translation
    })

# ---------------------------------------------------------
# Raw Frames
# ---------------------------------------------------------
@app.route("/rs/frame/depth")
def rs_frame_depth():
    frames = pipe.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    depth = np.asanyarray(depth_frame.get_data()).tolist()
    return jsonify({"depth": depth})

    
@app.route("/rs/frame/color")
def rs_frame_color():
    frames = pipe.wait_for_frames()
    color_frame = frames.get_color_frame()
    color = np.asanyarray(color_frame.get_data()).tolist()
    return jsonify({"color": color})

    
@app.route("/rs/frame/aligned")
def rs_frame_aligned():
    frames = pipe.wait_for_frames()
    aligned_frames = align.process(frames)

    depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    if not depth_frame or not color_frame:
        return jsonify({"error": "no_frames"}), 500

    # Convert frames safely on UNO Q
    depth = np.array(depth_frame.get_data(), dtype=np.uint16)
    color = np.array(color_frame.get_data(), dtype=np.uint8)

    # Return shapes explicitly
    return jsonify({
        "depth_shape": list(depth.shape),
        "color_shape": list(color.shape),
        "depth": depth.tolist(),
        "color": color.tolist()
    })


###################################################
# Pointcloud
###################################################
@app.route("/rs/pointcloud")
def rs_pointcloud():
    try:
        frames = pipe.wait_for_frames()
        aligned = align.process(frames)

        depth_frame = aligned.get_depth_frame()
        if not depth_frame:
            print("POINTCLOUD ERROR: no depth frame")
            return jsonify({"error": "no_depth_frame"}), 500

        pc = rs.pointcloud()
        pc.map_to(depth_frame)  # depth-only pointcloud

        points = pc.calculate(depth_frame)

        # BufData → NumPy structured array
        v = points.get_vertices()
        a = np.ctypeslib.as_array(v)

        # Convert structured array → Nx3 float32
        verts = np.zeros((a.shape[0], 3), dtype=np.float32)
        verts[:, 0] = a['f0']
        verts[:, 1] = a['f1']
        verts[:, 2] = a['f2']

        # Downsample
        verts = verts[::10]

        return jsonify({"points": verts.tolist()})

    except Exception as e:
        import traceback
        print("POINTCLOUD ERROR:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


###################################################
#  Deproject points
###################################################
@app.route("/rs/deproject/<int:x>/<int:y>/<float:depth_m>", methods=["GET"])
def rs_deproject(x, y, depth_m):
    try:
        global depth_intrinsics

        if depth_intrinsics is None:
            return jsonify({"status": "error", "message": "Intrinsics not initialized"}), 500

        intr = depth_intrinsics  # REAL struct

        # Validate pixel bounds
        if x < 0 or y < 0 or x >= intr.width or y >= intr.height:
            return jsonify({
                "status": "error",
                "message": f"Pixel ({x},{y}) out of bounds for {intr.width}x{intr.height}"
            }), 400

        pixel = [x, y]

        # Perform deprojection
        point = rs.rs2_deproject_pixel_to_point(intr, pixel, depth_m)

        return jsonify({
            "status": "ok",
            "pixel": pixel,
            "depth_m": depth_m,
            "point_xyz_m": {
                "x": float(point[0]),
                "y": float(point[1]),
                "z": float(point[2])
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



#####################################################
# Advanced Mode
#####################################################
@app.route("/rs/advanced_mode/status")
def rs_advanced_mode_status():
    try:
        ctx = rs.context()
        dev = ctx.query_devices()[0]
        adv = rs.rs400_advanced_mode(dev)
        return jsonify({"advanced_mode": adv.is_enabled()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/rs/advanced_mode/enable", methods=["POST"])
def rs_enable_advanced_mode():
    try:
        ctx = rs.context()
        dev = ctx.query_devices()[0]
        adv = rs.rs400_advanced_mode(dev)

        # Try enabling advanced mode
        adv.toggle_advanced_mode(True)

        # Wait for reboot
        import time
        time.sleep(5)

        # Re-discover device after reboot
        ctx = rs.context()
        devices = ctx.query_devices()
        if len(devices) == 0:
            return jsonify({"status": "error", "message": "No device after reboot"}), 500

        dev = devices[0]
        adv = rs.rs400_advanced_mode(dev)

        if not adv.is_enabled():
            return jsonify({"status": "error", "message": "Advanced mode still disabled"}), 500

        # Recreate pipeline and clear old state
        global pipe, profile, cfg, align
        pipe = rs.pipeline()
        profile = None
        cfg = None
        align = None

        return jsonify({"status": "advanced_mode_enabled"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route("/rs/advanced_mode/load_preset/<preset_name>", methods=["POST"])
def rs_load_named_preset(preset_name):
    try:
        import os

        ctx = rs.context()
        dev = ctx.query_devices()[0]
        adv = rs.rs400_advanced_mode(dev)

        # Build filename based on preset name
        filename = f"presets/{preset_name}.json"

        # Resolve absolute path for debugging
        abs_path = os.path.abspath(filename)
        cwd = os.getcwd()

        # Load preset JSON file
        with open(filename, "r") as f:
            preset_json = f.read()

        adv.load_json(preset_json)

        return jsonify({
            "status": "preset_loaded",
            "preset": preset_name,
            "path": abs_path,
            "cwd": cwd
        })

    except FileNotFoundError:
        import os

        cwd = os.getcwd()
        abs_path = os.path.abspath(f"presets/{preset_name}.json")

        # Try listing the presets directory
        try:
            preset_dir = os.listdir(os.path.join(cwd, "presets"))
        except Exception:
            preset_dir = "Could not list presets directory"

        return jsonify({
            "status": "error",
            "message": f"Preset '{preset_name}' not found",
            "cwd": cwd,
            "attempted_path": abs_path,
            "presets_dir_contents": preset_dir
        }), 404

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



####################
# set exposure and gain
@app.route("/rs/set/exposure/<int:value>", methods=["GET"])
def rs_set_exposure(value):
    try:
        color_sensor = _get_color_sensor()
        color_sensor.set_option(rs.option.exposure, value)
        return jsonify({"status": "ok", "exposure": value})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/rs/set/gain/<int:value>", methods=["GET"])
def rs_set_gain(value):
    try:
        color_sensor = _get_color_sensor()
        color_sensor.set_option(rs.option.gain, value)
        return jsonify({"status": "ok", "gain": value})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


####################
# set laser power
####################
@app.route("/rs/set/laser/<int:value>", methods=["GET"])
def rs_set_laser(value):
    try:
        depth_sensor = _get_depth_sensor()
        depth_sensor.set_option(rs.option.laser_power, value)
        return jsonify({"status": "ok", "laser_power": value})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

####################
# set emitter on/off
####################
@app.route("/rs/set/emitter/<int:onoff>", methods=["GET"])
def rs_set_emitter(onoff):
    try:
        depth_sensor = _get_depth_sensor()
        depth_sensor.set_option(rs.option.emitter_enabled, onoff)
        return jsonify({"status": "ok", "emitter": onoff})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



####################
# enable HDR
####################
@app.route("/rs/hdr/enable/<int:onoff>", methods=["GET"])
def rs_hdr_enable(onoff):
    try:
        global pipe, cfg
        if _pipeline_running():
            pipe.stop()

        depth_sensor = _get_depth_sensor()
        depth_sensor.set_option(rs.option.hdr_enabled, onoff)

        pipe.start(cfg)
        return jsonify({"status": "ok", "hdr_enabled": bool(onoff)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

####################
# Filter Options
####################
filters = {
    "decimation":        {"enabled": False, "filter": rs.decimation_filter()},
    "threshold":         {"enabled": False, "filter": rs.threshold_filter()},
    "depth2disparity":   {"enabled": False, "filter": rs.disparity_transform(True)},
    "spatial":           {"enabled": False, "filter": rs.spatial_filter()},
    "temporal":          {"enabled": False, "filter": rs.temporal_filter()},
    "hole_filling":      {"enabled": False, "filter": rs.hole_filling_filter()},
    "disparity2depth":   {"enabled": False, "filter": rs.disparity_transform(False)}
}

@app.route("/rs/filter_enable/<string:name>/<int:value>", methods=["GET"])
def rs_filter_enable(name, value):
    try:
        name = name.lower()
        if name not in filters:
            return jsonify({"status": "error", "message": f"Unknown filter '{name}'"}), 400

        filters[name]["enabled"] = bool(value)

        return jsonify({
            "status": "ok",
            "filter": name,
            "enabled": bool(value)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
        

@app.route("/rs/filter_apply", methods=["GET"])
def rs_filter_apply():
    try:
        global pipe, align, filters

        frames = pipe.wait_for_frames()
        aligned = align.process(frames)
        depth_frame = aligned.get_depth_frame()

        # Apply filters in order
        for name, f in filters.items():
            if f["enabled"]:
                depth_frame = f["filter"].process(depth_frame)

        return jsonify({"status": "ok", "message": "filters applied"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/rs/filter_threshold/<float:min_m>/<float:max_m>", methods=["GET"])
def rs_filter_threshold(min_m, max_m):
    try:
        # Ensure threshold filter exists
        if "threshold" not in filters:
            return jsonify({"status": "error", "message": "Threshold filter not found"}), 400

        # Update threshold filter options
        threshold_filter = filters["threshold"]["filter"]
        threshold_filter.set_option(rs.option.min_distance, min_m)
        threshold_filter.set_option(rs.option.max_distance, max_m)

        return jsonify({
            "status": "ok",
            "min_distance": min_m,
            "max_distance": max_m
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

################################################
#  White Balance
#################################################
@app.route("/rs/set/white_balance/<int:value>", methods=["GET"])
def rs_set_white_balance(value):
    try:
        color_sensor = _get_color_sensor()  # dev.query_sensors()[1]
        color_sensor.set_option(rs.option.white_balance, value)
        return jsonify({"status": "ok", "white_balance": value})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/rs/set/exposure_auto/<int:onoff>", methods=["GET"])
def rs_set_exposure_auto(onoff):
    try:
        color_sensor = _get_color_sensor()
        color_sensor.set_option(rs.option.enable_auto_exposure, onoff)
        return jsonify({"status": "ok", "auto_exposure": bool(onoff)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/rs/set/option/<string:name>/<value>", methods=["GET"])
def rs_set_option(name, value):
    try:
        value = float(value)

        # Build a safe lookup table of RealSense options
        option_map = {
            "exposure": rs.option.exposure,
            "gain": rs.option.gain,
            "white_balance": rs.option.white_balance,
            "enable_auto_exposure": rs.option.enable_auto_exposure,
            "laser_power": rs.option.laser_power,
            "emitter_enabled": rs.option.emitter_enabled,
            "hdr_enabled": rs.option.hdr_enabled
        }

        key = name.lower()
        if key not in option_map:
            return jsonify({"status": "error", "message": f"Unknown option '{name}'"}), 400

        option = option_map[key]

        # Decide which sensor receives the option
        if option in (
            rs.option.white_balance,
            rs.option.exposure,
            rs.option.gain,
            rs.option.enable_auto_exposure
        ):
            sensor = _get_color_sensor()
        else:
            sensor = _get_depth_sensor()

        sensor.set_option(option, value)

        return jsonify({"status": "ok", "option": name, "value": value})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500




@app.route("/rs/reset", methods=["POST"])
def rs_reset():
    try:
        dev = rs.context().query_devices()[0]
        dev.hardware_reset()
        return jsonify({"status": "ok", "message": "device reset"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

