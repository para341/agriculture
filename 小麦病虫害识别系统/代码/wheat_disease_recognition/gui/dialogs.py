import tkinter as tk
from tkinter import ttk, messagebox

from config import THEME, CONFIDENCE_THRESHOLD, CAMERA_INDEX, MODEL_PATH
import os


class SettingsDialog(tk.Toplevel):
    """设置对话框"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("系统设置")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.confidence = tk.DoubleVar(value=CONFIDENCE_THRESHOLD)
        self.camera_idx = tk.IntVar(value=CAMERA_INDEX)
        self.result = None

        self._create_widgets()
        self.center_on_parent(parent)

    def _create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # 置信度阈值
        ttk.Label(frame, text="置信度阈值:").grid(row=0, column=0, sticky=tk.W, pady=5)
        scale = ttk.Scale(frame, from_=0.1, to=0.9, variable=self.confidence,
                          orient=tk.HORIZONTAL, length=250)
        scale.grid(row=0, column=1, pady=5)
        ttk.Label(frame, textvariable=self.confidence).grid(row=0, column=2, padx=5)

        # 摄像头索引
        ttk.Label(frame, text="摄像头索引:").grid(row=1, column=0, sticky=tk.W, pady=5)
        spin = ttk.Spinbox(frame, from_=0, to=9, textvariable=self.camera_idx, width=5)
        spin.grid(row=1, column=1, sticky=tk.W, pady=5)

        # 模型路径
        ttk.Label(frame, text="模型路径:").grid(row=2, column=0, sticky=tk.W, pady=5)
        path_label = ttk.Label(frame, text=MODEL_PATH, wraplength=250,
                               foreground="gray")
        path_label.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)

        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=20)
        ttk.Button(btn_frame, text="确定", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def _on_ok(self):
        self.result = {
            "confidence": self.confidence.get(),
            "camera_index": self.camera_idx.get(),
        }
        self.destroy()

    def center_on_parent(self, parent):
        self.update_idletasks()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_x(), parent.winfo_y()
        w, h = 400, 300
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")


class AboutDialog(tk.Toplevel):
    """关于对话框"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("关于")
        self.geometry("400x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding=30)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="小麦病虫害识别系统",
                  font=("Microsoft YaHei", 16, "bold")).pack(pady=5)
        ttk.Label(frame, text="基于YOLOv8x的病虫害检测系统",
                  font=("Microsoft YaHei", 10)).pack(pady=5)
        ttk.Label(frame, text="识别类别: 叶锈病 | 健康 | 散黑穗病 | 黄锈病 | 秆锈病",
                  font=("Microsoft YaHei", 9)).pack(pady=5)
        ttk.Label(frame, text=f"王子涵  数据2301班",
                  font=("Microsoft YaHei", 9)).pack(pady=5)
        ttk.Label(frame, text="图像处理技术实验大作业",
                  font=("Microsoft YaHei", 9)).pack(pady=5)

        ttk.Button(self, text="确定", command=self.destroy).pack(pady=10)
        self.center_on_parent(parent)

    def center_on_parent(self, parent):
        self.update_idletasks()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_x(), parent.winfo_y()
        w, h = 400, 250
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
