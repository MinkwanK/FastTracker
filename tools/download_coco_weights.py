#!/usr/bin/env python3
"""
Download COCO pretrained weights for vehicle detection.

This script downloads the YOLOX-X model pretrained on COCO dataset,
which includes vehicle classes (car, bus, truck, motorcycle, bicycle, train).
"""

import os
import sys
import argparse
from pathlib import Path


# YOLOX COCO weights from official repository
YOLOX_WEIGHTS = {
    "yolox_x": {
        "url": "https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_x.pth",
        "filename": "yolox_x_coco.pth",
        "size": "~378MB"
    },
    "yolox_l": {
        "url": "https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_l.pth",
        "filename": "yolox_l_coco.pth",
        "size": "~207MB"
    },
    "yolox_m": {
        "url": "https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_m.pth",
        "filename": "yolox_m_coco.pth",
        "size": "~97MB"
    },
    "yolox_s": {
        "url": "https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.pth",
        "filename": "yolox_s_coco.pth",
        "size": "~35MB"
    }
}


def download_weights(model_name="yolox_x", output_dir="./pretrained"):
    """
    Download COCO pretrained weights.
    
    Args:
        model_name: Model size (yolox_x, yolox_l, yolox_m, yolox_s)
        output_dir: Directory to save the weights
    """
    if model_name not in YOLOX_WEIGHTS:
        print(f"Error: Model {model_name} not found.")
        print(f"Available models: {', '.join(YOLOX_WEIGHTS.keys())}")
        return False
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get model info
    model_info = YOLOX_WEIGHTS[model_name]
    output_file = output_path / model_info["filename"]
    
    # Check if file already exists
    if output_file.exists():
        print(f"✓ Weights already exist at: {output_file}")
        return True
    
    print(f"Downloading {model_name} weights ({model_info['size']})...")
    print(f"URL: {model_info['url']}")
    print(f"Output: {output_file}")
    
    try:
        # Download using urllib
        import urllib.request
        
        def reporthook(count, block_size, total_size):
            if total_size > 0:
                percent = int(count * block_size * 100 / total_size)
                sys.stdout.write(f"\rDownloading: {percent}%")
                sys.stdout.flush()
        
        urllib.request.urlretrieve(model_info["url"], output_file, reporthook)
        print("\n✓ Download completed successfully!")
        print(f"Weights saved to: {output_file}")
        return True
        
    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        print("\nPlease download manually from:")
        print(f"  {model_info['url']}")
        print(f"And save it to: {output_file}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download COCO pretrained weights for vehicle detection"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolox_x",
        choices=list(YOLOX_WEIGHTS.keys()),
        help="Model size to download (default: yolox_x)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./pretrained",
        help="Output directory (default: ./pretrained)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("YOLOX COCO Pretrained Weights Downloader")
    print("=" * 60)
    print(f"\nModel: {args.model}")
    print(f"Size: {YOLOX_WEIGHTS[args.model]['size']}")
    print(f"Output directory: {args.output}")
    print("\nThese weights are pretrained on COCO dataset and include:")
    print("  - Vehicle classes: car, bus, truck, motorcycle, bicycle, train")
    print("  - Person class and other COCO classes")
    print("\n" + "=" * 60 + "\n")
    
    success = download_weights(args.model, args.output)
    
    if success:
        print("\n" + "=" * 60)
        print("✓ Setup complete!")
        print("=" * 60)
        print("\nYou can now run vehicle detection using:")
        print(f"  python tools/demo_track_vehicle.py video \\")
        print(f"    -f exps/default/{args.model}.py \\")
        print(f"    -c {args.output}/{YOLOX_WEIGHTS[args.model]['filename']} \\")
        print(f"    --path <your_video.mp4> \\")
        print(f"    --save_result")
        print("\nOr use webcam:")
        print(f"  python tools/demo_track_vehicle.py webcam \\")
        print(f"    -f exps/default/{args.model}.py \\")
        print(f"    -c {args.output}/{YOLOX_WEIGHTS[args.model]['filename']} \\")
        print(f"    --camid 0")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
