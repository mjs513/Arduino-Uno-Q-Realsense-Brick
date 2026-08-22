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
