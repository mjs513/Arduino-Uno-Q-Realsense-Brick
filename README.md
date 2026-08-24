# UNO‑Q RealSense Flask API + Streamlit Viewer

This project provides a clean, modular RealSense pipeline for the UNO‑Q using:

- A Flask microservice (`app.py`) exposing RealSense functionality
- A Python client wrapper (`init.py`)

---

## Features

### ✔ RealSense Pipeline Control
- Initialize, configure, start, stop
- Depth + color streaming
- Depth aligned to color
- Intrinsics, extrinsics, depth scale

### ✔ Depth Processing
- Spatial, temporal, threshold, hole‑filling filters
- Disparity transforms
- Pixel → XYZ deprojection
- Pointcloud generation

### ✔ Sensor Controls
- Exposure, gain, white balance
- Laser power, emitter enable
- HDR mode
- Advanced mode + preset loading

### ✔ Streamlit Visualization
- Fast OpenCV colormap (Turbo, Jet, Inferno, etc.)
- Plotly depth histogram
- Color + depth side‑by‑side
- FPS counter
- Depth range slider

---
# App Structure
```text  
.
└── realsense_brick
    ├── app.yaml
    ├── bricks
    │   └── pyrealsense
    │       ├── app
    │       │   ├── app.py
    │       │   ├── presets
    │       │   │   ├── d4xx-default.json
    │       │   │   ├── d4xx-high-accuracy.json
    │       │   │   └── d4xx-high-confidence.json
    │       │   ├── __pycache__
    │       │   │   └── main.cpython-313.pyc
    │       │   └── requirements.txt
    │       ├── brick_compose.yaml
    │       ├── brick_config.yaml
    │       ├── Dockerfile
    │       ├── __init__.py
    │       ├── __pycache__
    │       │   └── __init__.cpython-313.pyc
    │       └── README.md
    ├── python
    │   ├── main.py
    │   └── requirements.txt
    ├── README.md
    ├── Samples
    │   ├── function_test.py
    │   ├── obs_avoid_convert_test.py
    │   └── Streamlit-cv2
    │       ├── README.md
    │       └── st_cv2.py
    └── sketch
        ├── sketch.ino
        └── sketch.yaml
```

## Install Rules file

Note I added a copy of the rules file that you can copy to the Arduino Uno Q 4GB

Create rules file
```bash
nano 99-realsense-libusb.rules
```
Copy and paste the following into the file  
```text
##Version=1.1##
# Device rules for Intel RealSense devices (R200, F200, SR300 LR200, ZR300, D400, L500, T200)
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0a80", MODE:="0666", GROUP:="plugdev", RUN+="/usr/local/bin/usb-R200-in_udev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0a66", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0aa3", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0aa2", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0aa5", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0abf", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0acb", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0ad0", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="04b4", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0ad1", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0ad2", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0ad3", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0ad4", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0ad5", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0ad6", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0af2", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0af6", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0afe", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0aff", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b00", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b01", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b03", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b07", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b0c", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b0d", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b3a", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b3d", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b48", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b49", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b4b", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b4d", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b52", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b56", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b5b", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b5c", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b64", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b68", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b6a", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b6b", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="1155", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="1156", MODE:="0666", GROUP:="plugdev"

# RealSense VID (0x38E5) D500-family devices
SUBSYSTEMS=="usb", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c01", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c02", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c03", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c04", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c05", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c06", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c07", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c08", MODE:="0666", GROUP:="plugdev"

# Intel RealSense recovery devices (DFU)
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0ab3", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0adb", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0adc", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0ade", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b55", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0add", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0cfd", MODE:="0666", GROUP:="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0cfe", MODE:="0666", GROUP:="plugdev"

# Intel RealSense devices (Movidius, T265)
SUBSYSTEMS=="usb", ENV{DEVTYPE}=="usb_device", ATTRS{idVendor}=="8087", ATTRS{idProduct}=="0af3", MODE="0666", GROUP="plugdev"
SUBSYSTEMS=="usb", ENV{DEVTYPE}=="usb_device", ATTRS{idVendor}=="8087", ATTRS{idProduct}=="0b37", MODE="0666", GROUP="plugdev"
SUBSYSTEMS=="usb", ENV{DEVTYPE}=="usb_device", ATTRS{idVendor}=="03e7", ATTRS{idProduct}=="2150", MODE="0666", GROUP="plugdev"

KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0ad5", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor_custom", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0ad5", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0af2", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0af2", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0afe", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor_custom", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0afe", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0aff", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor_custom", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0aff", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b00", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor_custom", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b00", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b01", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor_custom", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b01", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b3a", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b3a", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b3d", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b3d", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b4b", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b4b", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b4d", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b4d", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b56", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b56", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b5b", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b5b", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b5c", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b5c", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b64", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b64", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b68", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b68", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b6a", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b6a", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b6b", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b6b", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="1156", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="1156", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c01", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c01", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c02", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c02", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c03", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c03", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c04", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c04", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c05", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c05", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c06", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c06", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c07", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c07", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"
KERNEL=="iio*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c08", MODE:="0777", GROUP:="plugdev", RUN+="/bin/sh -c 'chmod -R 0777 /sys/%p'"
DRIVER=="hid_sensor*", ATTRS{idVendor}=="38e5", ATTRS{idProduct}=="0c08", RUN+="/bin/sh -c ' chmod -R 0777 /sys/%p && chmod 0777 /dev/%k'"

# For products with motion_module, if (kernels is 4.15 and up) and (device name is "accel_3d") wait, in another process, until (enable flag is set to 1 or 200 mSec passed) and then set it to 0.
KERNEL=="iio*", ATTRS{idVendor}=="8086|38e5", ATTRS{idProduct}=="0ad5|0afe|0aff|0b00|0b01|0b3a|0b3d|0b56|0b5c|0b64|0b68|0b6a|0b6b|1156|0c01|0c02|0c03|0c04|0c05|0c06|0c07|0c08", RUN+="/bin/sh -c '(major=`uname -r | cut -d \".\" -f1` && minor=`uname -r | cut -d \".\" -f2` && (([ $$major -eq 4 ] && [ $$minor -ge 15 ]) || [ $$major -ge 5 ])) && (enamefile=/sys/%p/name && [ `cat $$enamefile` = \"accel_3d\" ]) && enfile=/sys/%p/buffer/enable && echo \"COUNTER=0; while [ \$$COUNTER -lt 20 ] && grep -q 0 $$enfile; do sleep 0.01; COUNTER=\$$((COUNTER+1)); done && echo 0 > $$enfile\" | at now'"
```

Install and update
```bash
sudo cp 99-realsense-libusb.rules /etc/udev/99-realsense-libusb.rules/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Dockerfile layout
```  
FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git cmake build-essential \
    libusb-1.0-0-dev udev \
    python3-dev \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN git clone https://github.com/realsenseai/librealsense.git

WORKDIR /opt/librealsense

RUN mkdir build && cd build && \
    cmake .. \
      -DBUILD_PYTHON_BINDINGS=ON \
      -DPYTHON_EXECUTABLE=/usr/local/bin/python3 \
      -DFORCE_RSUSB_BACKEND=ON \
      -DBUILD_EXAMPLES=OFF \
      -DBUILD_TOOLS=OFF \
      -DBUILD_GRAPHICAL_EXAMPLES=OFF \
      -DBUILD_UNIT_TESTS=OFF \
      -DBUILD_WITH_OPENMP=OFF \
      -DBUILD_WITH_OPENGL=OFF \
      -DBUILD_WITH_QT=OFF \
      -DBUILD_WITH_OPENCL=OFF \
      -DBUILD_WITH_OPENSSL=OFF \
      -DBUILD_WITH_CUDA=OFF \
      -DBUILD_WITH_ZLIB=OFF \
      -DBUILD_SHARED_LIBS=OFF \
    && make -j$(nproc) \
    && make install

ENV PYTHONPATH=/usr/local/lib:/usr/local/lib/python3.13/site-packages

# App Lab brick layout
WORKDIR /app
COPY app .

RUN pip install -r requirements.txt
RUN pip install opencv-contrib-python-headless

# See: https://flask.palletsprojects.com/en/stable/cli/
CMD ["flask", "run", "--host", "0.0.0.0"]
```

1.  librealsense/pyrealsense is a minimal install of the librealsens disabling:
- C+tools
- C+examples
- OpenGL viewer
- Qt viewer
- CUDA
- OpenCL
- OpenSSL
- Zlib
- Shared libs
2. Installs the Python module into /usr/local/lib/python3.13/site-packages. Sets the pythonpath so it can be imported.
3. Installs `opencv-contrib-python-headless` into the app along with flask

##  Preset Directory
This directory contains realsense presets.  See [D400 Series Visual Presets](https://github.com/realsenseai/librealsense/wiki/D400-Series-Visual-Presets)

## Docker Compose file
```yaml
services:
  pyrealsense:
    build:
      context: .
    devices:
      - "/dev/bus/usb:/dev/bus/usb"
    privileged: true
    volumes:
    - /dev:/dev
    device_cgroup_rules:
    - 'c 81:* rmw'
    - 'c 189:* rmw'
    working_dir: /app
    restart: unless-stopped

    ports:
      - 5000:5000
```
The interesting thing in the compose file is that `device_cgroup_rules`.  This was extracted from the docker compose file from the ROS2 implementation to allow `advance_mode` to reboot and reconnect to USB.

## Samples
```text
├── Samples
│   ├── function_test.py
│   ├── obs_avoid_convert_test.py
│   └── Streamlit-cv2
│       ├── README.md
│       └── st_cv2.py
```
1. function_test.py - test of subset of functions to verify app is working
2. obs_avoid_convert_test.py - text only version of the 5x5 grid distances
3. st-cv2.py - streamlit realsense viewer.  Also a readme to add streamlit brick and requirements.txt file that sits next to the python script.

---

# ⭐ **RealSense Flask API Cross‑Matrix**  

## 🟦 **Pipeline Initialization & Configuration**

| init.py Function | Flask Endpoint | RealSense SDK Call | Meaning / Usage |
|------------------|----------------|--------------------|-----------------|
| `init(align_to)` | `/rs/init` | `pipe = rs.pipeline()`<br>`align = rs.align(rs.stream.color or depth)` | Creates pipeline object and alignment processor. Must be called first. |
| `configure(depth, color)` | `/rs/configure` | `cfg = rs.config()`<br>`cfg.enable_stream(rs.stream.depth, ...)`<br>`cfg.enable_stream(rs.stream.color, ...)` | Defines stream formats, resolutions, FPS. Must be called before `start()`. |
| `start()` | `/rs/start` | `profile = pipe.start(cfg)`<br>`intrinsics = profile.get_stream(...).intrinsics` | Starts streaming. Loads intrinsics. |
| `stop()` | `/rs/stop` | `pipe.stop()` | Stops pipeline. |

---

## 🟦 **Device & Sensor Info**

| init.py Function | Flask Endpoint | RealSense SDK Call | Meaning |
|------------------|----------------|--------------------|---------|
| `enumerateDevices()` | `/rs/enumerate` | `ctx.query_devices()` | Lists connected RealSense devices. |
| `getIntrinsics()` | `/rs/intrinsics` | `profile.get_stream(rs.stream.depth).get_intrinsics()` | Returns depth intrinsics (fx, fy, ppx, ppy). |
| `getExtrinsics()` | `/rs/extrinsics` | `depth_stream.get_extrinsics_to(color_stream)` | Returns transform from depth → color. |
| `getDepthScale()` | `/rs/get_depth_scale` | `depth_sensor.get_depth_scale()` | Returns depth scale (meters per unit). |

---

## 🟦 **Raw Frames**

| init.py Function | Flask Endpoint | RealSense SDK Call | Meaning |
|------------------|----------------|--------------------|---------|
| `getDepthFrame()` | `/rs/frame/depth` | `frames = pipe.wait_for_frames()`<br>`frames.get_depth_frame()` | Raw depth (not aligned, not filtered). |
| `getColorFrame()` | `/rs/frame/color` | `frames.get_color_frame()` | Raw color (BGR). |
| `getAlignedFrames()` | `/rs/frame/aligned` | `aligned = align.process(frames)` | Depth aligned to color. Still **unfiltered**. |

---

## 🟦 **Pointcloud**

| init.py Function | Flask Endpoint | RealSense SDK Call | Meaning |
|------------------|----------------|--------------------|---------|
| `getPointcloud()` | `/rs/pointcloud` | `pc = rs.pointcloud()`<br>`pc.calculate(depth_frame)` | Returns XYZ vertices from depth. |

---

## 🟦 **Pixel → 3D Deprojection**

| init.py Function | Flask Endpoint | RealSense SDK Call | Meaning |
|------------------|----------------|--------------------|---------|
| `deprojectPixel(x,y,depth_m)` | `/rs/deproject/<x>/<y>/<depth_m>` | `rs.rs2_deproject_pixel_to_point(intrinsics, [x,y], depth_m)` | Converts pixel + depth → real‑world XYZ. |

---

## 🟦 **Filters**

| init.py Function | Flask Endpoint | RealSense SDK Call | Meaning |
|------------------|----------------|--------------------|---------|
| `enableFilter(name, value)` | `/rs/filter_enable/<name>/<value>` | `filters[name]["enabled"] = bool(value)` | Enables/disables filter. |
| `applyFilters()` | `/rs/filter_apply` | `depth_frame = filter.process(depth_frame)` | Applies enabled filters in order. |
| `setFilterThreshold(min,max)` | `/rs/filter_threshold/<min>/<max>` | `threshold_filter.set_option(min_distance, max_distance)` | Sets min/max depth range. |

### Filters available:
- `decimation_filter`
- `threshold_filter`
- `disparity_transform(True)`
- `spatial_filter`
- `temporal_filter`
- `hole_filling_filter`
- `disparity_transform(False)`

---

## 🟦 **Advanced Mode & Presets**

| init.py Function | Flask Endpoint | RealSense SDK Call | Meaning |
|------------------|----------------|--------------------|---------|
| `advancedModeStatus()` | `/rs/advanced_mode/status` | `rs.rs400_advanced_mode(dev).is_enabled()` | Checks if advanced mode is enabled. |
| `enableAdvancedMode()` | `/rs/advanced_mode/enable` | `adv.toggle_advanced_mode(True)` | Enables advanced mode (device reboots). |
| `loadPreset(name)` | `/rs/advanced_mode/load_preset/<name>` | `adv.load_json(preset_json)` | Loads preset JSON file. |

---

## 🟦 **Sensor Options (Exposure, Gain, Laser, Emitter, HDR)**

| init.py Function | Flask Endpoint | RealSense SDK Call | Meaning |
|------------------|----------------|--------------------|---------|
| `setExposure(value)` | `/rs/set/exposure/<value>` | `color_sensor.set_option(rs.option.exposure, value)` | Manual exposure. |
| `setGain(value)` | `/rs/set/gain/<value>` | `color_sensor.set_option(rs.option.gain, value)` | Manual gain. |
| `setLaserPower(value)` | `/rs/set/laser/<value>` | `depth_sensor.set_option(rs.option.laser_power, value)` | IR emitter power. |
| `setEmitter(onoff)` | `/rs/set/emitter/<onoff>` | `depth_sensor.set_option(rs.option.emitter_enabled, onoff)` | IR emitter on/off. |
| `setHDR(onoff)` | `/rs/hdr/enable/<onoff>` | `depth_sensor.set_option(rs.option.hdr_enabled, onoff)` | HDR depth mode. |
| `setWhiteBalance(value)` | `/rs/set/white_balance/<value>` | `color_sensor.set_option(rs.option.white_balance, value)` | Manual white balance. |
| `setExposureAuto(onoff)` | `/rs/set/exposure_auto/<onoff>` | `color_sensor.set_option(rs.option.enable_auto_exposure, onoff)` | Auto exposure toggle. |
| `setOption(name,value)` | `/rs/set/option/<name>/<value>` | Generic option setter | Unified interface for exposure, gain, WB, laser, emitter, HDR. |

---

## 🟦 **Reset**

| init.py Function | Flask Endpoint | RealSense SDK Call | Meaning |
|------------------|----------------|--------------------|---------|
| `reset()` | `/rs/reset` | `dev.hardware_reset()` | Full hardware reset. |

---

# ⭐ **Usage Guide (How to use the matrix)**

### ✔ Typical pipeline startup sequence
```python
rsw.enableAdvancedMode()
rsw.loadPreset("d4xx-high-accuracy")

rsw.init(align_to="color")
rsw.configure(depth=(640,480,30,"z16"), color=(640,480,30,"bgr8"))
rsw.start()

scale = rsw.getDepthScale()
intr = rsw.getIntrinsics()
```

### ✔ Getting frames
```python
frame = rsw.getAlignedFrames()
depth = frame["depth"]
color = frame["color"]
```

### ✔ Applying filters
```python
rsw.enableFilter("spatial", 1)
rsw.enableFilter("temporal", 1)
rsw.enableFilter("threshold", 1)
rsw.setFilterThreshold(0.1, 10.0)
rsw.applyFilters()
```

### ✔ Deprojecting a pixel
```python
xyz = rsw.deprojectPixel(x, y, depth_m)
```

### ✔ Getting a pointcloud
```python
pc = rsw.getPointcloud()
```

---
