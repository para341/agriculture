#!/usr/bin/env python3
"""
小麦病虫害识别系统 - Web 后端
基于 Flask + YOLOv8x，提供三步流程：选图→预处理预览→YOLO识别
"""
import base64
import io
import os
import time
from pathlib import Path

import cv2
import numpy as np
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ultralytics import YOLO

# 添加项目路径以导入预处理模块
import sys
PROJ_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                        "代码", "wheat_disease_recognition")
if PROJ_DIR not in sys.path:
    sys.path.insert(0, PROJ_DIR)

from core.preprocessor import Preprocessor

app = Flask(__name__, static_folder="static")
CORS(app)

# 模型路径
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                          "代码", "wheat_disease_recognition", "models", "de_ide.pt")
CLASS_NAMES = {0: "叶锈病", 1: "健康", 2: "散黑穗病", 3: "黄锈病", 4: "秆锈病"}
CLASS_COLORS = {
    0: (255, 0, 0),    # 叶锈病 - 红 (OpenCV BGR)
    1: (0, 200, 0),    # 健康 - 绿
    2: (0, 165, 255),  # 散黑穗病 - 橙
    3: (0, 255, 255),  # 黄锈病 - 黄
    4: (255, 0, 0),    # 秆锈病 - 蓝
}

preprocessor = Preprocessor()

# 加载模型
print("正在加载模型...")
model = YOLO(MODEL_PATH)
model(np.zeros((320, 320, 3), dtype=np.uint8), verbose=False)
print("模型加载完成！")


def read_image_from_request(request):
    """从请求中读取图片，返回OpenCV图像"""
    file = request.files['file']
    file_bytes = file.read()
    np_arr = np.frombuffer(file_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


def get_preprocess_options(request):
    """从请求表单中获取预处理选项"""
    return {
        "clahe": request.form.get("clahe") == "1",
        "gaussian_blur": request.form.get("gaussian_blur") == "1",
        "sharpen": request.form.get("sharpen") == "1",
        "canny": request.form.get("canny") == "1",
        "gamma": request.form.get("gamma") == "1",
        "morphology": request.form.get("morphology") == "1",
    }


def image_to_base64(image: np.ndarray) -> str:
    """OpenCV图像 -> base64字符串"""
    _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return base64.b64encode(buffer).decode('utf-8')


def annotate_image(image: np.ndarray, result) -> np.ndarray:
    """在图像上绘制检测框和标签"""
    annotated = image.copy()
    boxes = result[0].boxes
    if boxes is None or len(boxes) == 0:
        return annotated

    for box in boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        color = CLASS_COLORS.get(cls_id, (255, 255, 255))
        label = f"{CLASS_NAMES.get(cls_id, '未知')} {conf:.1%}"

        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(annotated, (x1, y1 - th - 8), (x1 + tw + 8, y1), color, -1)
        cv2.putText(annotated, label, (x1 + 4, y1 - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    return annotated


@app.route('/')
def index():
    return send_file(str(Path(__file__).parent / 'index.html'))


@app.route('/preview', methods=['POST'])
def preview():
    """预处理预览接口：接收图片+预处理选项，返回预处理后的图像"""
    if 'file' not in request.files:
        return jsonify({"error": "没有上传文件"}), 400

    image = read_image_from_request(request)
    if image is None:
        return jsonify({"error": "无法解码图片"}), 400

    opts = get_preprocess_options(request)
    processed = preprocessor.preprocess(image, opts)

    # 返回预处理后的图像和原图
    return jsonify({
        "success": True,
        "original_image": image_to_base64(image),
        "processed_image": image_to_base64(processed),
        "original_size": {"w": image.shape[1], "h": image.shape[0]},
    })


@app.route('/preview-all', methods=['POST'])
def preview_all():
    """预处理分步预览：返回原图、每个选中方法的单独效果、综合效果"""
    if 'file' not in request.files:
        return jsonify({"error": "没有上传文件"}), 400

    image = read_image_from_request(request)
    if image is None:
        return jsonify({"error": "无法解码图片"}), 400

    opts = get_preprocess_options(request)

    # 每个独立方法的效果
    individual = {}
    method_map = {
        "clahe": ("CLAHE直方图均衡化", preprocessor.apply_clahe),
        "gaussian_blur": ("高斯滤波去噪", preprocessor.gaussian_blur),
        "sharpen": ("拉普拉斯锐化", preprocessor.sharpen),
        "canny": ("Canny边缘检测", preprocessor.apply_canny),
        "gamma": ("伽马校正", preprocessor.gamma_correction),
        "morphology": ("形态学开运算", preprocessor.morphology_open),
    }
    for key, (label, func) in method_map.items():
        if opts.get(key):
            result = func(image)
            individual[key] = {
                "label": label,
                "image": image_to_base64(result),
            }

    # 综合效果
    combined = preprocessor.preprocess(image, opts)

    return jsonify({
        "success": True,
        "original_image": image_to_base64(image),
        "individual": individual,
        "combined_image": image_to_base64(combined),
        "original_size": {"w": image.shape[1], "h": image.shape[0]},
    })


@app.route('/detect', methods=['POST'])
def detect():
    """接收上传图片+预处理选项，返回检测结果"""
    if 'file' not in request.files:
        return jsonify({"error": "没有上传文件"}), 400

    image = read_image_from_request(request)
    if image is None:
        return jsonify({"error": "无法解码图片"}), 400

    # 自动应用基础预处理（CLAHE+高斯滤波），提升YOLO检测效果
    # 同时叠加用户手动勾选的额外选项
    user_opts = get_preprocess_options(request)
    detect_opts = {"clahe": True, "gaussian_blur": True}
    for k in ["sharpen", "canny", "gamma", "morphology"]:
        if user_opts.get(k):
            detect_opts[k] = True
    processed = preprocessor.preprocess(image, detect_opts)

    # YOLO检测
    start = time.perf_counter()
    results = model(processed, conf=0.25, iou=0.45, verbose=False)
    infer_ms = round((time.perf_counter() - start) * 1000, 1)

    # 解析结果
    detections = []
    boxes_data = results[0].boxes
    if boxes_data and len(boxes_data) > 0:
        for box in boxes_data:
            cls_id = int(box.cls[0])
            conf = round(float(box.conf[0]), 4)
            x1, y1, x2, y2 = map(float, box.xyxy[0])
            detections.append({
                "class_id": cls_id,
                "class_name": CLASS_NAMES.get(cls_id, "未知"),
                "confidence": conf,
                "bbox": [round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1)],
            })

    # 标注图像
    annotated = annotate_image(processed, results)

    return jsonify({
        "success": True,
        "inference_time_ms": infer_ms,
        "object_count": len(detections),
        "detections": detections,
        "original_image": image_to_base64(image),
        "processed_image": image_to_base64(processed),
        "annotated_image": image_to_base64(annotated),
        "applied_preprocessing": [k for k, v in detect_opts.items() if v],
        "original_size": {"w": image.shape[1], "h": image.shape[0]},
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
