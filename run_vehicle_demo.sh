#!/bin/bash
# Example script to run vehicle detection demo
# This script demonstrates how to use the vehicle-only tracking demo

# Prerequisites:
# 1. Download pretrained weights (e.g., bytetrack_x_mot17.pth.tar) and place in pretrained/ folder
# 2. Prepare a video file for testing
# 3. Install required dependencies: pip install -r requirements.txt

# Example 1: Test with video file
python tools/demo_track_vehicle.py video \
    -f exps/example/mot/yolox_x_mix_det.py \
    -c pretrained/bytetrack_x_mot17.pth.tar \
    --path ./videos/test_traffic.mp4 \
    --fp16 \
    --fuse \
    --save_result

# Example 2: Test with webcam (real-time)
# python tools/demo_track_vehicle.py webcam \
#     -f exps/example/mot/yolox_x_mix_det.py \
#     -c pretrained/bytetrack_x_mot17.pth.tar \
#     --camid 0 \
#     --fp16 \
#     --fuse \
#     --save_result

# Example 3: Test with image sequence
# python tools/demo_track_vehicle.py image \
#     -f exps/example/mot/yolox_x_mix_det.py \
#     -c pretrained/bytetrack_x_mot17.pth.tar \
#     --path ./images/traffic_sequence/ \
#     --fp16 \
#     --fuse \
#     --save_result

# Notes:
# - The script will only detect and track vehicles (cars, buses, trucks, motorcycles, bicycles, trains)
# - Press 'q' or 'ESC' to quit the demo
# - Results will be saved in YOLOX_outputs/<experiment_name>/track_vis/ if --save_result is used
# - The model must be trained on COCO classes or a dataset containing vehicle categories
