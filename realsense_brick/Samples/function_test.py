import time
import pyrealsense as rs


def apply_high_accuracy():
    print("=== Applying High Accuracy Preset ===")
    
    # Color sensor auto exposure OFF
    print("Auto Exposure OFF:", rs.setExposureAuto(0))
    
    # Depth sensor controls (now working)
    print("Emitter ON:", rs.setEmitter(1))
    print("Laser Power:", rs.setLaserPower(150))
    
    # Color sensor manual exposure/gain
    print("Exposure:", rs.setExposure(8500))
    print("Gain:", rs.setGain(16))



def apply_extra_controls():
    print("=== Applying Extra Controls ===")

    print("  White Balance:", rs.setWhiteBalance(4500))
    print("  Auto Exposure OFF:", rs.setExposureAuto(0))

    print("  Generic Option Setter:")
    print("    Exposure:", rs.setOption("exposure", 8500))
    print("    Gain:", rs.setOption("gain", 16))


def main():
    print("=== RealSense Client ===")
    
    print("Devices:")
    devices = rs.printEnumeratedDevices()
    
    if devices and "devices" in devices and len(devices["devices"]) > 0:
        dev = devices["devices"][0]
    
        name = dev["name"]
        serial = dev["serial_number"]
        fw = dev["firmware_version"]
        port = dev["physical_port"]
        pid = dev["product_id"]
    
        print(
            f"=== RealSense Device ===\n"
            f"\tName:\t{dev['name']}\n"
            f"\tSerial:\t{dev['serial_number']}\n"
            f"\tFirmware:\t{dev['firmware_version']}\n"
            f"\tPort:\t{dev['physical_port']}\n"
            f"\tProduct ID:\t{dev['product_id']}\n"
        )

    
    print("Status:", rs.status())
    
    # MUST BE FIRST Test Advanced Mode
    print("Enabling advanced mode...")
    print(rs.enableAdvancedMode())
    
    print("Checking advanced mode status...")
    adv_status = rs.advancedModeStatus()
    print("Advanced Mode Status:", adv_status)
    
    if not adv_status.get("advanced_mode"):
        print("ERROR: Advanced mode is not enabled. Stopping.")
        return
    
    print("Advanced mode verified.")


    # Test manual commands
    #apply_high_accuracy()
    #apply_extra_controls()

    print("Loading preset...")
    print(rs.loadPreset("d4xx-high-accuracy"))

    
    print("Initializing pipeline...")
    print(rs.init(align_to="color"))
    
    print("Configuring streams...")
    print(rs.configure(
        depth=(640, 480, 30, "z16"),
        color=(640, 480, 30, "bgr8")
    ))
    
    print("Starting pipeline...")
    print(rs.start())

    print("Depth Scale:", rs.getDepthScale())
    print("Intrinsics:", rs.getIntrinsics())

    rs.enableFilter("decimation", 1)
    rs.enableFilter("threshold", 1)
    rs.enableFilter("depth2disparity", 1)
    rs.enableFilter("spatial", 1)
    rs.enableFilter("temporal", 1)
    rs.enableFilter("hole_filling", 1)
    rs.enableFilter("disparity2depth", 1)
    print("Testing filters")
    print("Applying filters:", rs.applyFilters())


    frame = rs.getAlignedFrames()
    print("Depth shape:", frame.get("depth_shape"))
    print("Color shape:", frame.get("color_shape"))

    print("Stopping pipeline...")
    print(rs.stop())

    while True:
        time.sleep(5)


if __name__ == "__main__":
    main()
