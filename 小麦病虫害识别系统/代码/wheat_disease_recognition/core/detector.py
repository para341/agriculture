from dataclasses import dataclass, field
from typing import List, Optional

import cv2
import numpy as np
from ultralytics import YOLO

from config import CLASS_NAMES, CONFIDENCE_THRESHOLD, IOU_THRESHOLD


@dataclass
class DetectionResult:
    """检测结果数据类"""
    class_ids: List[int] = field(default_factory=list)
    class_names: List[str] = field(default_factory=list)
    confidences: List[float] = field(default_factory=list)
    boxes: List[List[float]] = field(default_factory=list)  # [x1,y1,x2,y2]
    annotated_image: Optional[np.ndarray] = None  # 标注后的图像
    raw_image: Optional[np.ndarray] = None       # 原始图像
    inference_time_ms: float = 0.0

    def object_count(self) -> int:
        """返回检测到的目标数量"""
        return len(self.class_ids)

    def summary(self) -> str:
        """返回检测结果的文本摘要"""
        if self.object_count() == 0:
            return "未检测到目标"
        lines = []
        for name, conf in zip(self.class_names, self.confidences):
            lines.append(f"{name}: {conf:.1%}")
        return " | ".join(lines)


class Detector:
    """YOLO模型封装，负责模型加载、推理和结果解析"""

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.class_names = CLASS_NAMES

    def load_model(self):
        """加载YOLO模型并进行预热"""
        self.model = YOLO(self.model_path)
        # 预热：用空白图像推理一次，加载模型到GPU
        dummy = np.zeros((320, 320, 3), dtype=np.uint8)
        self.model(dummy, verbose=False)
        return self

    def detect(self, image: np.ndarray) -> DetectionResult:
        """对单张图像进行检测，返回结构化结果"""
        import time
        start = time.perf_counter()
        results = self.model(
            image,
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,
            verbose=False,
        )
        infer_time = (time.perf_counter() - start) * 1000

        result = DetectionResult(inference_time_ms=round(infer_time, 1))
        if not results or len(results) == 0:
            result.raw_image = image
            result.annotated_image = image.copy()
            return result

        boxes_data = results[0].boxes
        if boxes_data is None or len(boxes_data) == 0:
            result.raw_image = image
            result.annotated_image = image.copy()
            return result

        # 解析检测结果
        for box in boxes_data:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(float, box.xyxy[0])
            result.class_ids.append(cls_id)
            result.class_names.append(self.class_names.get(cls_id, f"未知({cls_id})"))
            result.confidences.append(conf)
            result.boxes.append([x1, y1, x2, y2])

        # 使用YOLO自带的标注图像
        result.annotated_image = results[0].plot()
        result.raw_image = image.copy()

        return result

    def detect_batch(self, images: List[np.ndarray], callback=None) -> List[DetectionResult]:
        """批量检测图像，支持进度回调"""
        all_results = []
        total = len(images)
        for i, img in enumerate(images):
            res = self.detect(img)
            all_results.append(res)
            if callback:
                callback(i + 1, total, res)
        return all_results
