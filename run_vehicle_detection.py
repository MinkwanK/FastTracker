#!/usr/bin/env python3
"""
간단한 차량 객체 검지 실행 스크립트 (Simple Vehicle Detection Launcher)

이 스크립트는 차량 객체 검지를 쉽게 실행할 수 있도록 도와줍니다.
This script helps you easily run vehicle object detection.

사용법 (Usage):
    # 웹캠 사용 (Use webcam)
    python run_vehicle_detection.py

    # 비디오 파일 사용 (Use video file)
    python run_vehicle_detection.py --video path/to/video.mp4

    # 결과 저장 (Save results)
    python run_vehicle_detection.py --save
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def check_weights():
    """Check if COCO weights are available."""
    pretrained_dir = Path("./pretrained")
    weights_files = [
        "yolox_x_coco.pth",
        "yolox_l_coco.pth",
        "yolox_m_coco.pth",
        "yolox_s_coco.pth",
        "yolox_x.pth",
        "yolox_l.pth",
        "yolox_m.pth",
        "yolox_s.pth",
    ]
    
    for weight_file in weights_files:
        weight_path = pretrained_dir / weight_file
        if weight_path.exists():
            return str(weight_path)
    
    return None


def download_weights():
    """Download COCO weights if not available."""
    print("\n" + "=" * 60)
    print("COCO 가중치를 찾을 수 없습니다.")
    print("COCO weights not found.")
    print("=" * 60)
    print("\n지금 다운로드하시겠습니까? (Do you want to download now?)")
    print("  [y] Yes - Download yolox_x (recommended, ~378MB)")
    print("  [s] Download yolox_s (smaller, ~35MB)")
    print("  [n] No - Exit")
    
    choice = input("\n선택 (Choice) [y/s/n]: ").lower().strip()
    
    if choice == 'y':
        model = "yolox_x"
    elif choice == 's':
        model = "yolox_s"
    else:
        print("\n프로그램을 종료합니다. (Exiting.)")
        return None
    
    print(f"\n{model} 가중치를 다운로드합니다... (Downloading {model} weights...)")
    
    try:
        result = subprocess.run(
            [sys.executable, "tools/download_coco_weights.py", "--model", model],
            check=True
        )
        
        # Check again after download
        weight_path = check_weights()
        if weight_path:
            print(f"\n✓ 다운로드 완료! (Download complete!)")
            return weight_path
        else:
            print("\n✗ 다운로드 실패 (Download failed)")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 다운로드 중 오류 발생: {e}")
        print("✗ Error during download")
        return None
    except KeyboardInterrupt:
        print("\n\n다운로드 취소됨 (Download cancelled)")
        return None


def get_exp_file(weight_path):
    """Get the corresponding experiment file for the weight."""
    weight_name = Path(weight_path).stem  # e.g., yolox_x_coco or yolox_x
    
    # Extract base model name (yolox_x, yolox_l, etc.)
    if "_coco" in weight_name:
        base_name = weight_name.replace("_coco", "")
    else:
        base_name = weight_name
    
    exp_file = f"exps/default/{base_name}.py"
    
    if not Path(exp_file).exists():
        # Try with yolox_x as fallback
        exp_file = "exps/default/yolox_x.py"
    
    return exp_file


def run_vehicle_detection(args):
    """Run the vehicle detection demo."""
    
    # Check for weights
    weight_path = check_weights()
    
    if not weight_path:
        print("\n가중치 파일을 찾을 수 없습니다. (Weight file not found.)")
        weight_path = download_weights()
        
        if not weight_path:
            print("\n프로그램을 종료합니다. (Exiting.)")
            return 1
    
    # Get experiment file
    exp_file = get_exp_file(weight_path)
    
    # Build command
    cmd = [
        sys.executable,
        "tools/demo_track_vehicle.py",
    ]
    
    # Add demo type and path
    if args.video:
        cmd.extend(["video", "--path", args.video])
    else:
        cmd.extend(["webcam", "--camid", str(args.camid)])
    
    # Add model files
    cmd.extend([
        "-f", exp_file,
        "-c", weight_path,
    ])
    
    # Add optional flags
    if args.save:
        cmd.append("--save_result")
    
    cmd.extend(["--fp16", "--fuse"])
    
    # Print info
    print("\n" + "=" * 60)
    print("차량 객체 검지 시작 (Starting Vehicle Detection)")
    print("=" * 60)
    print(f"\n모델 (Model): {Path(weight_path).name}")
    print(f"실험 파일 (Experiment): {exp_file}")
    
    if args.video:
        print(f"입력 (Input): 비디오 파일 (Video file) - {args.video}")
    else:
        print(f"입력 (Input): 웹캠 (Webcam) - 카메라 {args.camid}")
    
    if args.save:
        print("출력 (Output): 결과 저장됨 (Results will be saved)")
    else:
        print("출력 (Output): 실시간 표시만 (Display only)")
    
    print("\n검지 대상 (Detection targets):")
    print("  - 자동차 (car)")
    print("  - 버스 (bus)")
    print("  - 트럭 (truck)")
    print("  - 오토바이 (motorcycle)")
    print("  - 자전거 (bicycle)")
    print("  - 기차 (train)")
    
    print("\n종료: 'q' 또는 'ESC' 키 (Exit: press 'q' or 'ESC')")
    print("=" * 60 + "\n")
    
    # Run the command
    try:
        subprocess.run(cmd, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 오류 발생 (Error occurred): {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\n프로그램 종료 (Exiting)")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="차량 객체 검지 실행 (Run Vehicle Object Detection)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제 (Examples):
  # 웹캠으로 실행 (Run with webcam)
  python run_vehicle_detection.py

  # 비디오 파일로 실행 (Run with video file)
  python run_vehicle_detection.py --video video.mp4

  # 결과 저장하며 실행 (Run and save results)
  python run_vehicle_detection.py --video video.mp4 --save

  # 다른 웹캠 사용 (Use different webcam)
  python run_vehicle_detection.py --camid 1
        """
    )
    
    parser.add_argument(
        "--video",
        type=str,
        default=None,
        help="비디오 파일 경로 (Path to video file). 생략시 웹캠 사용 (If omitted, uses webcam)"
    )
    
    parser.add_argument(
        "--camid",
        type=int,
        default=0,
        help="웹캠 ID (Webcam ID, default: 0)"
    )
    
    parser.add_argument(
        "--save",
        action="store_true",
        help="결과 저장 (Save detection results)"
    )
    
    args = parser.parse_args()
    
    # Print welcome message
    print("\n" + "=" * 60)
    print("FastTracker - 차량 객체 검지 (Vehicle Object Detection)")
    print("=" * 60)
    
    return run_vehicle_detection(args)


if __name__ == "__main__":
    sys.exit(main())
