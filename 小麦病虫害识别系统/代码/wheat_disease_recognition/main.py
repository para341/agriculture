#!/usr/bin/env python3
"""
小麦病虫害识别系统
基于YOLOv8x的病虫害检测系统
王子涵  数据2301班
"""

import sys
import os

# 确保项目根目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import MODEL_PATH
from core.detector import Detector
from gui.app import MainWindow


def main():
    print("正在加载模型...")
    detector = Detector(MODEL_PATH)
    detector.load_model()
    print("模型加载完成！")

    app = MainWindow(detector)
    app.run()


if __name__ == "__main__":
    main()
