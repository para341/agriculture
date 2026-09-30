import threading
import time
import cv2
from queue import Queue, Empty

from core.detector import Detector


class CameraThread(threading.Thread):
    """摄像头实时检测线程，独立运行不阻塞GUI"""

    def __init__(self, detector: Detector, callback, camera_index=0):
        super().__init__(daemon=True)
        self.detector = detector
        self.callback = callback
        self.camera_index = camera_index
        self._running = threading.Event()
        self._stopped = threading.Event()
        self.fps = 0
        self._frame_count = 0
        self._fps_timer = time.time()

    def run(self):
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            self.callback(None, None, "无法打开摄像头")
            return

        self._running.set()
        self._frame_count = 0
        self._fps_timer = time.time()

        while self._running.is_set():
            ret, frame = cap.read()
            if not ret:
                continue

            # 检测
            result = self.detector.detect(frame)

            # 计算FPS
            self._frame_count += 1
            elapsed = time.time() - self._fps_timer
            if elapsed >= 1.0:
                self.fps = round(self._frame_count / elapsed, 1)
                self._frame_count = 0
                self._fps_timer = time.time()

            # 回调传递结果
            self.callback(result.annotated_image, result, None)

        cap.release()
        self._stopped.set()

    def stop(self):
        """停止摄像头线程"""
        self._running.clear()
        self._stopped.wait(timeout=2.0)
