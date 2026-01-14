# 차량 객체 검지 가이드 (Vehicle Object Detection Guide)

FastTracker를 사용하여 실시간으로 차량 객체를 검지하는 방법을 설명합니다.

## 빠른 시작 (Quick Start)

### 1. 환경 설정 (Environment Setup)

```bash
# FastTracker 환경 활성화
conda activate FastTracker

# 필요한 패키지가 설치되어 있지 않다면
pip install -r requirements.txt
python setup.py develop
```

### 2. 차량 검지 실행 (Run Vehicle Detection)

**가장 쉬운 방법 - 웹캠 사용 (Easiest way - Using Webcam):**

```bash
python run_vehicle_detection.py
```

**비디오 파일 사용 (Using Video File):**

```bash
python run_vehicle_detection.py --video your_video.mp4
```

**결과 저장하면서 실행 (Run and Save Results):**

```bash
python run_vehicle_detection.py --video your_video.mp4 --save
```

처음 실행하면 COCO 가중치를 자동으로 다운로드할지 물어봅니다. 'y'를 입력하면 자동으로 다운로드됩니다.

## 검지 가능한 차량 (Detectable Vehicles)

- 🚗 자동차 (car)
- 🚌 버스 (bus)
- 🚚 트럭 (truck)
- 🏍️ 오토바이 (motorcycle)
- 🚲 자전거 (bicycle)
- 🚂 기차 (train)

## 수동 설정 (Manual Setup)

자동 스크립트를 사용하지 않고 직접 실행하려면:

### 1단계: COCO 가중치 다운로드 (Download COCO Weights)

```bash
# yolox_x (큰 모델, 더 정확함, ~378MB)
python tools/download_coco_weights.py --model yolox_x

# 또는 yolox_s (작은 모델, 더 빠름, ~35MB)
python tools/download_coco_weights.py --model yolox_s
```

### 2단계: 차량 검지 데모 실행 (Run Vehicle Detection Demo)

**웹캠 사용 (Using Webcam):**

```bash
python tools/demo_track_vehicle.py webcam \
    -f exps/default/yolox_x.py \
    -c pretrained/yolox_x_coco.pth \
    --camid 0 \
    --fp16 \
    --fuse \
    --save_result
```

**비디오 파일 사용 (Using Video File):**

```bash
python tools/demo_track_vehicle.py video \
    -f exps/default/yolox_x.py \
    -c pretrained/yolox_x_coco.pth \
    --path ./videos/your_video.mp4 \
    --fp16 \
    --fuse \
    --save_result
```

**이미지 시퀀스 사용 (Using Image Sequence):**

```bash
python tools/demo_track_vehicle.py image \
    -f exps/default/yolox_x.py \
    -c pretrained/yolox_x_coco.pth \
    --path ./images/folder/ \
    --fp16 \
    --fuse \
    --save_result
```

## 명령줄 옵션 (Command Line Options)

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--path` | 비디오 파일 또는 이미지 폴더 경로 | - |
| `--camid` | 웹캠 카메라 ID | 0 |
| `--save_result` | 결과 저장 여부 | False |
| `--fp16` | FP16 정밀도 사용 (더 빠름) | False |
| `--fuse` | 모델 융합 (더 빠름) | False |
| `--track_thresh` | 추적 신뢰도 임계값 | 0.5 |
| `--track_buffer` | 추적 버퍼 프레임 수 | 30 |
| `--match_thresh` | 매칭 임계값 | 0.8 |

## 출력 결과 (Output Results)

결과는 다음 위치에 저장됩니다:

```
YOLOX_outputs/<experiment_name>/track_vis/<timestamp>/
├── output_video.mp4      # 검지 결과가 표시된 비디오
└── <timestamp>.txt       # 추적 결과 텍스트 파일 (MOT 형식)
```

추적 결과 형식 (Tracking result format):
```
<frame_id>,<track_id>,<x>,<y>,<width>,<height>,<confidence>,-1,-1,-1
```

## 실행 중 제어 (Runtime Controls)

- **종료 (Exit)**: `q` 또는 `ESC` 키를 누르세요
- 비디오/웹캠 창이 표시되며 실시간으로 차량이 검지되고 추적됩니다

## 문제 해결 (Troubleshooting)

### 1. "No module named 'cv2'" 오류

```bash
pip install opencv-python
```

### 2. "CUDA out of memory" 오류

더 작은 모델을 사용하거나 `--fp16` 옵션을 추가하세요:

```bash
python tools/download_coco_weights.py --model yolox_s
python run_vehicle_detection.py --video video.mp4  # yolox_s를 자동으로 사용
```

### 3. 웹캠이 작동하지 않음

다른 카메라 ID를 시도해보세요:

```bash
python run_vehicle_detection.py --camid 1
# 또는
python run_vehicle_detection.py --camid 2
```

### 4. 검지 결과가 없음

- MOT17/MOT20 가중치를 사용하고 있지 않은지 확인하세요 (보행자만 검지함)
- COCO 가중치를 사용해야 합니다: `yolox_x_coco.pth`

## 중요 참고사항 (Important Notes)

⚠️ **MOT17/MOT20 가중치는 사용하지 마세요!**

- `bytetrack_x_mot17.pth.tar`와 `bytetrack_x_mot20.pth.tar`는 보행자만 검지합니다
- 차량을 검지하려면 반드시 COCO 가중치를 사용해야 합니다

✅ **COCO 가중치 사용**

- `yolox_x_coco.pth` (또는 `yolox_x.pth`): COCO 데이터셋으로 학습
- 80개 클래스 포함 (차량 클래스 포함)

## 성능 팁 (Performance Tips)

1. **GPU 사용**: CUDA가 설치되어 있으면 자동으로 GPU를 사용합니다
2. **FP16 정밀도**: `--fp16` 옵션으로 속도 향상
3. **모델 융합**: `--fuse` 옵션으로 추가 속도 향상
4. **작은 모델**: `yolox_s`는 `yolox_x`보다 빠르지만 정확도는 낮습니다

## 고급 사용 (Advanced Usage)

### 설정 파일 사용 (Using Configuration File)

커스텀 추적 파라미터를 사용하려면 JSON 설정 파일을 만들 수 있습니다:

```bash
python tools/demo_track_vehicle.py video \
    -f exps/default/yolox_x.py \
    -c pretrained/yolox_x_coco.pth \
    --path video.mp4 \
    --config configs/custom_config.json \
    --save_result
```

설정 파일 예제 (`configs/custom_config.json`):

```json
{
    "track_thresh": 0.6,
    "track_buffer": 30,
    "match_thresh": 0.7,
    "min_box_area": 100
}
```

## 추가 도움말 (Additional Help)

더 자세한 정보는 메인 README.md 파일을 참조하세요:
- [README.md](README.md)
- [FastTracker Paper](https://arxiv.org/abs/2508.14370)
- [FastTracker Benchmark](https://huggingface.co/datasets/Hamidreza-Hashemp/FastTracker-Benchmark)
