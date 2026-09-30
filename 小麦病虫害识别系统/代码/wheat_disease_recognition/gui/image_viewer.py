
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np


class ImageViewer(tk.Canvas):
    """图像显示控件，支持缩放、平移、显示标注"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.config(bg="#f0f0f0")

        self._image = None
        self._photo = None
        self._scale_factor = 1.0
        self._offset_x = 0
        self._offset_y = 0
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._image_original = None

        # 绑定鼠标事件
        self.bind("<ButtonPress-1>", self._on_drag_start)
        self.bind("<B1-Motion>", self._on_drag_move)
        self.bind("<MouseWheel>", self._on_zoom)

        # 占位文字
        self._draw_placeholder()

    def _draw_placeholder(self, text="请上传图片进行检测"):
        """绘制占位文字"""
        self.delete("all")
        self.create_text(
            self.winfo_width() // 2 if self.winfo_width() > 1 else 200,
            self.winfo_height() // 2 if self.winfo_height() > 1 else 200,
            text=text,
            fill="#aaaaaa",
            font=("Microsoft YaHei", 16),
            tags="placeholder"
        )

    def display_image(self, image: np.ndarray):
        """显示OpenCV图像（BGR格式）"""
        if image is None:
            return
        # BGR -> RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self._image_original = image_rgb
        self._scale_factor = 1.0
        self._offset_x = 0
        self._offset_y = 0
        self._render_image()

    def display_raw_image(self, image: np.ndarray):
        """直接显示RGB图像"""
        self._image_original = image
        self._scale_factor = 1.0
        self._offset_x = 0
        self._offset_y = 0
        self._render_image()

    def _render_image(self):
        """根据缩放和平移参数渲染图像"""
        if self._image_original is None:
            return

        h, w = self._image_original.shape[:2]
        new_w = int(w * self._scale_factor)
        new_h = int(h * self._scale_factor)

        if new_w < 10 or new_h < 10:
            return

        pil_img = Image.fromarray(self._image_original)
        pil_img = pil_img.resize((new_w, new_h), Image.LANCZOS)
        self._photo = ImageTk.PhotoImage(pil_img)

        self.delete("all")
        self.create_image(
            self.winfo_width() // 2 + self._offset_x,
            self.winfo_height() // 2 + self._offset_y,
            image=self._photo,
            anchor="center",
            tags="image"
        )

    def _on_drag_start(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def _on_drag_move(self, event):
        dx = event.x - self._drag_start_x
        dy = event.y - self._drag_start_y
        self._offset_x += dx
        self._offset_y += dy
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self._render_image()

    def _on_zoom(self, event):
        # 鼠标滚轮缩放
        scale = 1.1 if event.delta > 0 else 0.9
        self._scale_factor *= scale
        self._scale_factor = max(0.1, min(5.0, self._scale_factor))
        self._render_image()

    def clear(self):
        """清空显示"""
        self._image_original = None
        self._photo = None
        self.delete("all")
        self._draw_placeholder()

    def fit_to_size(self):
        """自适应缩放至控件大小"""
        if self._image_original is None:
            return
        h, w = self._image_original.shape[:2]
        cw = self.winfo_width()
        ch = self.winfo_height()
        if cw > 0 and ch > 0:
            self._scale_factor = min(cw / w, ch / h) * 0.9
            self._offset_x = 0
            self._offset_y = 0
            self._render_image()


import cv2
