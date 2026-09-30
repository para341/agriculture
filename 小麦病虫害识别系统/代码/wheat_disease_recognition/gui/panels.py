import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

import cv2
import numpy as np
from PIL import Image, ImageTk

from config import (THEME, SUPPORTED_EXTENSIONS, DETECTIONS_DIR,
                    PREPROCESS_OPTIONS)
from core.detector import Detector
from core.preprocessor import Preprocessor
from core.statistics import DetectionStatistics
from gui.image_viewer import ImageViewer
from gui.camera_thread import CameraThread


class BasePanel(ttk.Frame):
    """面板基类，提供通用功能"""

    def __init__(self, parent, detector: Detector, stats: DetectionStatistics,
                 status_callback=None):
        super().__init__(parent)
        self.detector = detector
        self.stats = stats
        self.preprocessor = Preprocessor()
        self.status_callback = status_callback or (lambda msg: None)
        self._setup_style()

    def _setup_style(self):
        style = ttk.Style()
        style.configure("Accent.TButton", background=THEME["accent"],
                        foreground="white")
        style.configure("Sidebar.TFrame", background=THEME["sidebar"])
        style.configure("Card.TFrame", background=THEME["card"],
                        relief="solid", borderwidth=1)

    def set_status(self, msg: str):
        self.status_callback(msg)


class ImageModePanel(BasePanel):
    """图像检测模式面板 — 三步流程：选图→预处理预览→YOLO识别"""

    def __init__(self, parent, detector, stats, status_callback=None):
        super().__init__(parent, detector, stats, status_callback)
        self._current_image = None
        self._current_result = None
        self._preprocess_vars = {}
        self._current_mode = "empty"  # empty / original / preview / detected
        self._setup_ui()

    def _setup_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ─── 左侧控制面板 ───
        left = ttk.Frame(self, width=220, padding=10)
        left.grid(row=0, column=0, sticky="nswe")
        left.grid_propagate(False)

        ttk.Label(left, text="图像检测", font=("Microsoft YaHei", 12, "bold")).pack(anchor=tk.W)

        # 步骤1: 文件操作
        step1 = ttk.LabelFrame(left, text="① 选择图片", padding=8)
        step1.pack(fill=tk.X, pady=4)
        ttk.Button(step1, text="选择图片", command=self._select_image).pack(fill=tk.X, pady=2)

        # 步骤2: 预处理预览
        step2 = ttk.LabelFrame(left, text="② 预处理预览", padding=8)
        step2.pack(fill=tk.X, pady=4)
        for key, opt in PREPROCESS_OPTIONS.items():
            var = tk.BooleanVar(value=opt["default"])
            self._preprocess_vars[key] = var
            cb = ttk.Checkbutton(step2, text=opt["label"], variable=var,
                                 command=self._on_preprocess_changed)
            cb.pack(anchor=tk.W, pady=1)
        ttk.Label(step2, text="勾选后自动更新预览", font=("Microsoft YaHei", 8),
                  foreground="#999999").pack(anchor=tk.W)

        # 步骤3: YOLO识别
        step3 = ttk.LabelFrame(left, text="③ YOLO识别", padding=8)
        step3.pack(fill=tk.X, pady=4)
        self._btn_detect = ttk.Button(step3, text="🚀 执行YOLO识别",
                                      command=self._run_detection,
                                      style="Accent.TButton")
        self._btn_detect.pack(fill=tk.X, pady=2)

        # 结果操作
        result_frame = ttk.LabelFrame(left, text="结果操作", padding=8)
        result_frame.pack(fill=tk.X, pady=4)
        ttk.Button(result_frame, text="保存结果",
                   command=self._save_result).pack(fill=tk.X, pady=2)
        ttk.Button(result_frame, text="清空",
                   command=self._clear).pack(fill=tk.X, pady=2)

        # ─── 右侧显示区 ───
        right = ttk.Frame(self, padding=10)
        right.grid(row=0, column=1, sticky="nswe")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        self.viewer = ImageViewer(right, bg=THEME["bg"])
        self.viewer.grid(row=0, column=0, sticky="nswe")

        # 模式标签
        self._mode_label = ttk.Label(right, text="状态：等待加载图片",
                                     font=("Microsoft YaHei", 9, "bold"),
                                     foreground=THEME["sidebar"])
        self._mode_label.grid(row=1, column=0, sticky="w", pady=(2, 0))

        # 结果信息
        self.info_text = tk.Text(right, height=6, font=("Microsoft YaHei", 9),
                                 state="disabled", wrap=tk.WORD)
        self.info_text.grid(row=2, column=0, sticky="ew", pady=(5, 0))

    # ──────── 事件响应 ────────

    def _on_preprocess_changed(self):
        """预处理选项变化时，自动更新预览图"""
        if self._current_image is None:
            return
        opts = {k: v.get() for k, v in self._preprocess_vars.items()}
        # 只要有任意一个预处理被选中，就显示预处理结果
        any_checked = any(opts.values())
        if any_checked:
            processed = self.preprocessor.preprocess(self._current_image, opts)
            self.viewer.display_image(processed)
            self._current_mode = "preview"
            self._update_mode_label("预处理结果")
            checked_names = [opt["label"] for key, opt in PREPROCESS_OPTIONS.items()
                             if opts.get(key)]
            self._update_info("预处理已应用: " + " | ".join(checked_names))
            self.set_status("预处理预览 | " + " | ".join(checked_names))
        else:
            # 全部取消则回到原图
            self.viewer.display_image(self._current_image)
            self._current_mode = "original"
            self._update_mode_label("原始图像")
            self._update_info("未应用预处理，显示原始图像")
            self.set_status("原始图像")

    def _select_image(self):
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp"), ("所有文件", "*.*")]
        )
        if not path:
            return
        self._load_and_display(path)

    def _select_folder(self):
        folder = filedialog.askdirectory(title="选择图片文件夹")
        if not folder:
            return
        files = [os.path.join(folder, f) for f in os.listdir(folder)
                 if f.lower().endswith(SUPPORTED_EXTENSIONS)]
        if not files:
            messagebox.showinfo("提示", "文件夹中没有支持的图片文件")
            return
        self._image_list = files
        self._current_idx = 0
        self._load_and_display(files[0])

    def _load_and_display(self, path: str):
        image = cv2.imread(path)
        if image is None:
            messagebox.showerror("错误", f"无法加载图片: {path}")
            return
        self._current_image = image
        self._current_image_path = path
        self._current_result = None
        self._current_mode = "original"
        self.viewer.display_image(image)
        self._update_mode_label("原始图像")
        self.set_status(f"已加载: {os.path.basename(path)} ({image.shape[1]}x{image.shape[0]})")
        self._update_info("图片已加载 ✓  可在左侧勾选预处理选项查看中间效果，然后点击「YOLO识别」获得检测结果")

    def _run_detection(self):
        if self._current_image is None:
            messagebox.showinfo("提示", "请先选择图片")
            return

        # 先应用当前预处理
        preprocess_opts = {k: v.get() for k, v in self._preprocess_vars.items()}
        processed = self.preprocessor.preprocess(self._current_image, preprocess_opts)

        # YOLO检测
        self.set_status("正在检测...")
        result = self.detector.detect(processed)
        self._current_result = result
        self.stats.add_result(result)

        # 显示检测结果
        if result.annotated_image is not None:
            self.viewer.display_image(result.annotated_image)
        self._current_mode = "detected"
        self._update_mode_label("检测结果（YOLO标注）")
        self.set_status(f"检测完成 | 耗时: {result.inference_time_ms}ms | "
                        f"目标数: {result.object_count()}")

        # 更新信息
        self._update_result_info(result)

    def _update_mode_label(self, mode_text):
        """更新界面上的模式标签"""
        self._mode_label.config(text=f"当前显示: {mode_text}")

    def _update_result_info(self, result):
        info = f"检测耗时: {result.inference_time_ms}ms\n"
        info += f"检测目标数: {result.object_count()}\n"
        info += "-" * 30 + "\n"
        for name, conf in zip(result.class_names, result.confidences):
            info += f"  {name}: {conf:.1%}\n"
        self._update_info(info)

    def _update_info(self, text):
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)
        self.info_text.config(state="disabled")

    def _save_result(self):
        if self._current_result is None:
            messagebox.showinfo("提示", "没有检测结果可保存")
            return
        os.makedirs(DETECTIONS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(DETECTIONS_DIR, f"result_{timestamp}.jpg")
        if self._current_result.annotated_image is not None:
            cv2.imwrite(path, self._current_result.annotated_image)
            self.set_status(f"结果已保存: {path}")
            messagebox.showinfo("保存成功", f"结果已保存至:\n{path}")

    def _clear(self):
        self._current_image = None
        self._current_result = None
        self._current_mode = "empty"
        self.viewer.clear()
        self._update_mode_label("等待加载图片")
        self._update_info("")
        self.set_status("已清空")


class CameraModePanel(BasePanel):
    """摄像头实时检测模式面板"""

    def __init__(self, parent, detector, stats, status_callback=None,
                 camera_index=0):
        self.camera_index = camera_index
        super().__init__(parent, detector, stats, status_callback)
        self._camera_thread = None
        self._is_running = False
        self._setup_ui()

    def _setup_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # 左侧控制面板
        left = ttk.Frame(self, width=220, padding=10)
        left.grid(row=0, column=0, sticky="nswe")
        left.grid_propagate(False)

        ttk.Label(left, text="摄像头检测", font=("Microsoft YaHei", 12, "bold")).pack(anchor=tk.W)

        # 控制按钮
        ctrl_frame = ttk.LabelFrame(left, text="控制", padding=8)
        ctrl_frame.pack(fill=tk.X, pady=8)
        self._btn_start = ttk.Button(ctrl_frame, text="打开摄像头",
                                      command=self._toggle_camera)
        self._btn_start.pack(fill=tk.X, pady=2)
        ttk.Button(ctrl_frame, text="截图保存",
                   command=self._capture).pack(fill=tk.X, pady=2)

        # 状态显示
        status_frame = ttk.LabelFrame(left, text="状态", padding=8)
        status_frame.pack(fill=tk.X, pady=8)
        self._fps_label = ttk.Label(status_frame, text="FPS: --")
        self._fps_label.pack(anchor=tk.W)
        self._detect_label = ttk.Label(status_frame, text="检测目标: --")
        self._detect_label.pack(anchor=tk.W)

        # 右侧显示区
        right = ttk.Frame(self, padding=10)
        right.grid(row=0, column=1, sticky="nswe")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        self.viewer = ImageViewer(right, bg=THEME["bg"])
        self.viewer.grid(row=0, column=0, sticky="nswe")

        self._last_frame = None

    def _toggle_camera(self):
        if self._is_running:
            self._stop_camera()
        else:
            self._start_camera()

    def _start_camera(self):
        self._camera_thread = CameraThread(
            self.detector,
            self._on_camera_frame,
            camera_index=self.camera_index,
        )
        self._camera_thread.start()
        self._is_running = True
        self._btn_start.config(text="关闭摄像头")
        self.set_status("摄像头已开启")

    def _stop_camera(self):
        if self._camera_thread:
            self._camera_thread.stop()
            self._camera_thread = None
        self._is_running = False
        self._btn_start.config(text="打开摄像头")
        self.viewer.clear()
        self._fps_label.config(text="FPS: --")
        self._detect_label.config(text="检测目标: --")
        self.set_status("摄像头已关闭")

    def _on_camera_frame(self, annotated_frame, result, error):
        if error:
            self.set_status(f"错误: {error}")
            self._stop_camera()
            return
        if annotated_frame is not None:
            self._last_frame = annotated_frame
            self.viewer.display_image(annotated_frame)
            self._fps_label.config(text=f"FPS: {self._camera_thread.fps}")
            if result:
                self._detect_label.config(text=f"检测目标: {result.object_count()}")
                self.stats.add_result(result)

    def _capture(self):
        if self._last_frame is None:
            messagebox.showinfo("提示", "没有可保存的画面")
            return
        os.makedirs(DETECTIONS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(DETECTIONS_DIR, f"camera_{timestamp}.jpg")
        cv2.imwrite(path, self._last_frame)
        self.set_status(f"截图已保存: {path}")

    def update_camera_index(self, index: int):
        self.camera_index = index


class BatchModePanel(BasePanel):
    """批量处理模式面板"""

    def __init__(self, parent, detector, stats, status_callback=None):
        super().__init__(parent, detector, stats, status_callback)
        self._file_list = []
        self._setup_ui()

    def _setup_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # 顶部控制栏
        top = ttk.Frame(self, padding=10)
        top.grid(row=0, column=0, sticky="ew")
        ttk.Button(top, text="选择文件夹",
                   command=self._select_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(top, text="开始批量处理",
                   command=self._run_batch).pack(side=tk.LEFT, padx=2)
        ttk.Button(top, text="导出CSV报告",
                   command=self._export_csv).pack(side=tk.LEFT, padx=2)
        ttk.Button(top, text="清空列表",
                   command=self._clear_list).pack(side=tk.LEFT, padx=2)

        # 进度条
        self._progress = ttk.Progressbar(top, mode="determinate", length=300)
        self._progress.pack(side=tk.RIGHT, padx=5)
        self._progress_label = ttk.Label(top, text="0/0")
        self._progress_label.pack(side=tk.RIGHT)

        # 文件列表
        list_frame = ttk.Frame(self, padding=10)
        list_frame.grid(row=1, column=0, sticky="nswe")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self._tree = ttk.Treeview(list_frame,
                                   columns=("file", "status", "count"),
                                   show="headings", height=20)
        self._tree.heading("file", text="文件名")
        self._tree.heading("status", text="状态")
        self._tree.heading("count", text="检测数")
        self._tree.column("file", width=400)
        self._tree.column("status", width=100, anchor="center")
        self._tree.column("count", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                  command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.grid(row=0, column=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def _select_folder(self):
        folder = filedialog.askdirectory(title="选择图片文件夹")
        if not folder:
            return
        self._file_list = [os.path.join(folder, f) for f in os.listdir(folder)
                          if f.lower().endswith(SUPPORTED_EXTENSIONS)]
        self._refresh_tree()
        self.set_status(f"已加载 {len(self._file_list)} 张图片")

    def _refresh_tree(self):
        self._tree.delete(*self._tree.get_children())
        for path in self._file_list:
            self._tree.insert("", tk.END, values=(os.path.basename(path), "待处理", "-"))

    def _run_batch(self):
        if not self._file_list:
            messagebox.showinfo("提示", "请先选择图片文件夹")
            return

        self._progress["maximum"] = len(self._file_list)
        self._progress["value"] = 0

        for idx, path in enumerate(self._file_list):
            image = cv2.imread(path)
            if image is None:
                continue
            result = self.detector.detect(image)
            self.stats.add_result(result)

            # 更新树状视图
            item = self._tree.get_children()[idx]
            self._tree.item(item, values=(
                os.path.basename(path), "已完成", result.object_count()
            ))

            # 更新进度
            self._progress["value"] = idx + 1
            self._progress_label.config(text=f"{idx + 1}/{len(self._file_list)}")
            self.set_status(f"处理中: {os.path.basename(path)} ({idx + 1}/{len(self._file_list)})")
            self.update()

        self.set_status("批量处理完成")

    def _export_csv(self):
        if not self.stats.history:
            messagebox.showinfo("提示", "没有检测数据可导出")
            return
        path = self.stats.export_csv()
        self.set_status(f"报告已导出: {path}")
        messagebox.showinfo("导出成功", f"CSV报告已保存至:\n{path}")

    def _clear_list(self):
        self._file_list = []
        self._tree.delete(*self._tree.get_children())
        self._progress["value"] = 0
        self._progress_label.config(text="0/0")
        self.set_status("已清空")


class HistoryPanel(BasePanel):
    """检测历史面板"""

    def __init__(self, parent, detector, stats, status_callback=None):
        super().__init__(parent, detector, stats, status_callback)
        self._setup_ui()

    def _setup_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        frame = ttk.Frame(self, padding=10)
        frame.grid(row=0, column=0, sticky="nswe")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        ttk.Label(frame, text="检测统计", font=("Microsoft YaHei", 12, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 10))

        text_frame = ttk.Frame(frame)
        text_frame.grid(row=1, column=0, sticky="nswe")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self._text = tk.Text(text_frame, font=("Microsoft YaHei", 10),
                             state="disabled", wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL,
                                  command=self._text.yview)
        self._text.configure(yscrollcommand=scrollbar.set)
        self._text.grid(row=0, column=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, pady=10)
        ttk.Button(btn_frame, text="刷新统计",
                   command=self._refresh).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="导出CSV",
                   command=self._export).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清空统计",
                   command=self._clear_stats).pack(side=tk.LEFT, padx=5)

    def _refresh(self):
        dist = self.stats.get_class_distribution()
        conf_stats = self.stats.get_confidence_stats()

        text = "=== 类别分布 ===\n"
        for name, count in dist.items():
            text += f"  {name}: {count} 个\n"

        text += f"\n=== 置信度统计 ===\n"
        text += f"  总检测数: {conf_stats['count']}\n"
        text += f"  最小: {conf_stats['min']:.3f}\n"
        text += f"  最大: {conf_stats['max']:.3f}\n"
        text += f"  平均: {conf_stats['avg']:.3f}\n"

        text += f"\n=== 检测次数 ===\n"
        text += f"  共处理 {len(self.stats.history)} 次检测\n"

        self._text.config(state="normal")
        self._text.delete(1.0, tk.END)
        self._text.insert(1.0, text)
        self._text.config(state="disabled")
        self.set_status("统计已刷新")

    def _export(self):
        if not self.stats.history:
            messagebox.showinfo("提示", "没有检测数据")
            return
        path = self.stats.export_csv()
        self.set_status(f"已导出: {path}")
        messagebox.showinfo("导出成功", f"统计已导出至:\n{path}")

    def _clear_stats(self):
        if messagebox.askyesno("确认", "确定清空所有统计记录?"):
            self.stats.clear()
            self._refresh()
            self.set_status("统计已清空")
