#!/usr/bin/env python3

import sys
import time
import signal
import argparse
import numpy as np

# Your Flask wrapper client
import pyrealsense as rsw

######################################################
##  Depth parameters                                ##
######################################################

DEPTH_WIDTH   = 640
DEPTH_HEIGHT  = 480
COLOR_WIDTH   = 640
COLOR_HEIGHT  = 480
FPS           = 30
DEPTH_RANGE_M = [0.1, 10.0]

GRID_ROWS     = 5
GRID_COLS     = 5
TOTAL_CELLS   = GRID_ROWS * GRID_COLS

USE_PRESET    = True
PRESET_NAME   = "d4xx-high-accuracy"

default_large_dist = 9999.0
main_loop_should_quit = False

######################################################
##  CLI                                             ##
######################################################

parser = argparse.ArgumentParser(description="RealSense Depth Processing via Wrapper")
args = parser.parse_args()

######################################################
##  Helpers                                         ##
######################################################

def progress(msg):
    print(f"INFO: {msg}", flush=True)

def send_data_placeholder(coordinates):
    """
    Print the 5x5 matrix of XYZ coordinates in a readable format.
    Coordinates is a flat list of 25 entries.
    Each entry is (z, y, x).
    """

    # Convert flat list → 5x5 grid
    grid = np.array(coordinates).reshape((GRID_ROWS, GRID_COLS, 3))

    print("\n=== 5x5 Coordinate Grid (Z,Y,X in meters) ===")
    for r in range(GRID_ROWS):
        row_str = ""
        for c in range(GRID_COLS):
            z, y, x = grid[r, c]
            if z >= default_large_dist:
                row_str += "   ---   "
            else:
                row_str += f"{z:0.2f} "
        print(row_str)
    print("============================================\n")


def sigint_handler(sig, frame):
    global main_loop_should_quit
    main_loop_should_quit = True

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

######################################################
##  Grid + depth math                               ##
######################################################

def distances_from_depth_image(depth_mat,
                               min_depth_m,
                               max_depth_m,
                               depth,
                               depth_coordinates,
                               depth_scale_val,
                               rows,
                               cols):

    h, w = depth_mat.shape
    step_x = max(1, int(w / 40))
    step_y = max(1, int(h / 40))

    grid_w = w // cols
    grid_h = h // rows

    for i in range(rows * cols):
        row = i // cols
        col = i % cols

        sx = col * grid_w
        sy = row * grid_h
        ex = sx + grid_w
        ey = sy + grid_h

        sub = depth_mat[sy:ey:step_y, sx:ex:step_x] * depth_scale_val
        valid = (sub > min_depth_m) & (sub < max_depth_m)

        if np.any(valid):
            min_val = np.min(sub[valid])
            depth[i] = min_val

            idx = np.argwhere((sub == min_val) & valid)[0]
            ypix = sy + idx[0] * step_y
            xpix = sx + idx[1] * step_x
            depth_coordinates[i] = [ypix, xpix]

    return depth_coordinates, depth

def convert_depth_to_phys_coord_using_realsense(depth_coordinates, depth_m):
    """
    Uses Flask endpoint /rs/deproject/<x>/<y>/<depth_m>
    """
    x = int(depth_coordinates[1])
    y = int(depth_coordinates[0])

    resp = rsw.deprojectPixel(x, y, depth_m)

    if "point_xyz_m" not in resp:
        return (default_large_dist, default_large_dist, default_large_dist)

    p = resp["point_xyz_m"]
    return (p["z"], p["y"], p["x"])

######################################################
##  Main                                            ##
######################################################

def main():
    global main_loop_should_quit

    progress("Enabling advanced mode...")
    print(rsw.enableAdvancedMode())
    #time.sleep(5)

    if USE_PRESET:
        progress(f"Loading preset: {PRESET_NAME}")
        print(rsw.loadPreset(PRESET_NAME))

    progress("Initializing pipeline...")
    print(rsw.init(align_to="color"))
    print(rsw.configure(
        depth=(DEPTH_WIDTH, DEPTH_HEIGHT, FPS, "z16"),
        color=(COLOR_WIDTH, COLOR_HEIGHT, FPS, "bgr8")
    ))
    print(rsw.start())

    depth_scale = rsw.getDepthScale()["depth_scale_m"]
    intrinsics  = rsw.getIntrinsics()

    progress(f"Depth scale: {depth_scale}")
    progress(f"Intrinsics: {intrinsics}")

    progress("Configuring filters...")
    rsw.enableFilter("decimation", 1)
    rsw.enableFilter("threshold", 1)
    rsw.setFilterThreshold(DEPTH_RANGE_M[0], DEPTH_RANGE_M[1])
    rsw.enableFilter("depth2disparity", 1)
    rsw.enableFilter("spatial", 1)
    rsw.enableFilter("temporal", 1)
    rsw.enableFilter("hole_filling", 0)
    rsw.enableFilter("disparity2depth", 1)

    rsw.applyFilters()
    progress("Running ...")
    
    last_time = time.time()

    try:
        while not main_loop_should_quit:

            frame = rsw.getAlignedFrames()
            if not frame or "depth" not in frame:
                continue

            depth_mat = np.array(frame["depth"], dtype=np.uint16)

            depth_list = np.ones((TOTAL_CELLS,), dtype=np.float64) * (DEPTH_RANGE_M[1] + 1)
            depth_coords = np.ones((TOTAL_CELLS, 2), dtype=np.uint16) * int(default_large_dist)

            obstacle_list, depth_list = distances_from_depth_image(
                depth_mat,
                DEPTH_RANGE_M[0],
                DEPTH_RANGE_M[1],
                depth_list,
                depth_coords,
                depth_scale,
                GRID_ROWS,
                GRID_COLS
            )

            coord_list = np.ones((TOTAL_CELLS, 3), dtype=np.float64) * default_large_dist

            for i in range(len(depth_list)):
                if depth_list[i] < DEPTH_RANGE_M[1]:
                    coord_list[i] = convert_depth_to_phys_coord_using_realsense(
                        obstacle_list[i],
                        depth_list[i]
                    )

            send_data_placeholder(coord_list)

            last_time = time.time()

    except Exception as e:
        progress(f"Exception: {e}")

    finally:
        progress("Stopping pipeline...")
        try:
            rsw.stop()
        except:
            pass
        sys.exit(0)

if __name__ == "__main__":
    main()
