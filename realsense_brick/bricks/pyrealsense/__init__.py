import requests

# Base address of your RealSense Flask brick
BASE_URL = "http://pyrealsense:5000"

# ----------------------------------------------------
# Private Helper Utility
# ----------------------------------------------------
def _safe_get(url, timeout=2.0):
    """
    Safe GET wrapper with timeout + JSON fallback.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            return response.json()
        except Exception:
            return {"status": "error", "message": f"Server error ({response.status_code}): {e}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Network transport connection failed: {e}"}


def _safe_post(url, data=None, timeout=2.0):
    """
    Safe POST wrapper with timeout + JSON fallback.
    """
    try:
        response = requests.post(url, json=data, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        try:
            return response.json()
        except Exception:
            return {"status": "error", "message": f"POST failed: {e}"}


# --------------------------------------------------
# Initialize pipeline
# ---------------------------------------------------
def init(align_to="color"):
    payload = {"align_to": align_to}
    return _safe_post(f"{BASE_URL}/rs/init", data=payload, timeout=3.0)

# ----------------------------------------------------
# Config Control
# ----------------------------------------------------
def configure(
    depth=(640,480,30,"z16"),
    color=(640,480,30,"bgr8")
):
    payload = {
        "depth_width": depth[0],
        "depth_height": depth[1],
        "depth_fps": depth[2],
        "depth_format": depth[3],

        "color_width": color[0],
        "color_height": color[1],
        "color_fps": color[2],
        "color_format": color[3]
    }
    return _safe_post(f"{BASE_URL}/rs/configure", data=payload, timeout=5.0)


# ----------------------------------------------------
# Pipeline Control
# ----------------------------------------------------
def start():
    """Start RealSense pipeline."""
    return _safe_post(f"{BASE_URL}/rs/start", timeout=10)

def stop():
    """Stop RealSense pipeline."""
    return _safe_post(f"{BASE_URL}/rs/stop", timeout=5)

# ----------------------------------------------------
# Get enumerated devices
# ----------------------------------------------------
def enumerateDevices():
    return _safe_get(f"{BASE_URL}/rs/enumerate", timeout=5)

def printEnumeratedDevices():
    devices = enumerateDevices()
    print("=== Enumerated RealSense Devices ===")
    print(devices)
    return devices


# ----------------------------------------------------
# Context / Device / Camera Info
# ----------------------------------------------------
def getContext():
    return _safe_get(f"{BASE_URL}/rs/context")

def getDeviceInfo():
    return _safe_get(f"{BASE_URL}/rs/device_info")

def getCameraInfo():
    return _safe_get(f"{BASE_URL}/rs/camera_info")

def getProfile():
    return _safe_get(f"{BASE_URL}/rs/profile")


# ----------------------------------------------------
# Intrinsics / Extrinsics / Depth Scale
# ----------------------------------------------------
def getDepthIntrinsics():
    return _safe_get(f"{BASE_URL}/rs/get_depth_intrinsics")

def getIntrinsics():
    return _safe_get(f"{BASE_URL}/rs/intrinsics")

def getExtrinsics():
    return _safe_get(f"{BASE_URL}/rs/extrinsics")

def getDepthScale():
    return _safe_get(f"{BASE_URL}/rs/get_depth_scale")


# ----------------------------------------------------
# Raw Frames
# ----------------------------------------------------
def getDepthFrame():
    return _safe_get(f"{BASE_URL}/rs/frame/depth", timeout=1.0)

def getColorFrame():
    return _safe_get(f"{BASE_URL}/rs/frame/color", timeout=1.0)

def getAlignedFrames():
    return _safe_get(f"{BASE_URL}/rs/frame/aligned", timeout=10.0)


# ----------------------------------------------------
# Grid Processing (5×5 obstacle grid)
# ----------------------------------------------------
def getGrid():
    return _safe_get(f"{BASE_URL}/rs/grid", timeout=1.0)


# ----------------------------------------------------
# Filters
# ----------------------------------------------------
def enableFilter(name, value):
    return _safe_get(f"{BASE_URL}/rs/filter_enable/{name}/{value}")

def applyFilters():
    return _safe_get(f"{BASE_URL}/rs/filter_apply")

def setFilterThreshold(min_m, max_m):
    return _safe_get(f"{BASE_URL}/rs/filter_threshold/{min_m}/{max_m}")


# ----------------------------------------------------
# Advanced Mode / Presets
# ----------------------------------------------------
def advancedModeStatus():
    return _safe_get(f"{BASE_URL}/rs/advanced_mode/status", timeout=10)
    
def enableAdvancedMode():
    return _safe_post(f"{BASE_URL}/rs/advanced_mode/enable", timeout=10)

def loadPreset(name):
    return _safe_post(f"{BASE_URL}/rs/advanced_mode/load_preset/{name}", timeout=10)


# ----------------------------------------------------
# Sensor Options (Exposure, Gain, Laser, Emitter, HDR)
# ----------------------------------------------------
def setExposure(value):
    return _safe_get(f"{BASE_URL}/rs/set/exposure/{value}")

def setGain(value):
    return _safe_get(f"{BASE_URL}/rs/set/gain/{value}")

def setLaserPower(value):
    return _safe_get(f"{BASE_URL}/rs/set/laser/{value}")

def setEmitter(onoff):
    return _safe_get(f"{BASE_URL}/rs/set/emitter/{onoff}")

def setHDR(onoff):
    return _safe_get(f"{BASE_URL}/rs/hdr/enable/{onoff}")


# ----------------------------------------------------
# Pointcloud
# ----------------------------------------------------
def getPointcloud():
    return _safe_get(f"{BASE_URL}/rs/pointcloud", timeout=5.0)


# ----------------------------------------------------
# Pixel → 3D Deprojection
# ----------------------------------------------------
def deprojectPixel(x, y, depth_m):
    """
    Convert pixel coordinate + depth (meters) → XYZ point.
    """
    return _safe_get(f"{BASE_URL}/rs/deproject/{x}/{y}/{depth_m}")


# ----------------------------------------------------
# Status
# ----------------------------------------------------
def status():
    return _safe_get(f"{BASE_URL}/rs/status")

# ---------------------------------------------------
# white balance, Auto exposure, Generic Option setter
# reset, apply filter
# ----------------------------------------------------
def setWhiteBalance(value):
    return _safe_get(f"{BASE_URL}/rs/set/white_balance/{value}")

def setExposureAuto(onoff):
    return _safe_get(f"{BASE_URL}/rs/set/exposure_auto/{onoff}")

def setOption(name, value):
    return _safe_get(f"{BASE_URL}/rs/set/option/{name}/{value}")

def reset():
    return _safe_post(f"{BASE_URL}/rs/reset")

def applyFilters():
    return _safe_get(f"{BASE_URL}/rs/filter_apply")



