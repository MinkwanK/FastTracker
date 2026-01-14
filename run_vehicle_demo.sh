#!/bin/bash
# Example script to run vehicle detection demo
# This script demonstrates how to use the vehicle-only tracking demo

# Prerequisites:
# 1. Download COCO-pretrained weights or train a custom model with vehicle classes
#    NOTE: Standard MOT17/MOT20 weights (bytetrack_x_mot17.pth.tar) only detect pedestrians
#          and will NOT work with this vehicle-only demo!
#    
#    For vehicle detection, you need one of:
#    - COCO-pretrained YOLOX model (contains 80 classes including vehicles)
#    - Custom model trained on a multi-class dataset with vehicles (e.g., FastTracker benchmark)
#
# 2. Prepare a video file for testing
# 3. Install required dependencies: pip install -r requirements.txt

# Example 1: Test with video file using a COCO-pretrained model
# Replace 'yolox_x_coco.pth.tar' with your actual COCO model path
python tools/demo_track_vehicle.py video \
    -f exps/default/yolox_x.py \
    -c pretrained/yolox_x_coco.pth.tar \
    --path ./videos/test_traffic.mp4 \
    --fp16 \
    --fuse \
    --save_result

# Example 2: Test with webcam (real-time)
# python tools/demo_track_vehicle.py webcam \
#     -f exps/default/yolox_x.py \
#     -c pretrained/yolox_x_coco.pth.tar \
#     --camid 0 \
#     --fp16 \
#     --fuse \
#     --save_result

# Example 3: Test with image sequence
# python tools/demo_track_vehicle.py image \
#     -f exps/default/yolox_x.py \
#     -c pretrained/yolox_x_coco.pth.tar \
#     --path ./images/traffic_sequence/ \
#     --fp16 \
#     --fuse \
#     --save_result

# Notes:
# - The script will only detect and track vehicles (cars, buses, trucks, motorcycles, bicycles, trains)
# - Press 'q' or 'ESC' to quit the demo
# - Results will be saved in YOLOX_outputs/<experiment_name>/track_vis/ if --save_result is used
# - DO NOT use MOT17/MOT20 pretrained weights - they only detect pedestrians!
