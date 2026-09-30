import tkinter as tk
from tkinter import ttk, messagebox

from config import THEME, WINDOW_TITLE, WINDOW_SIZE, CONFIDENCE_THRESHOLD
from core.detector import Detector
from core.statistics import DetectionStatistics
from gui.panels import ImageModePanel, CameraModePanel, BatchModePanel, HistoryPanel
from gui.dialogs import SettingsDialog, AboutDialog


class MainWindow:
    """主窗口，管理布局和页面切换"""

    def __init__(self, detector: Detector):
        self.detector = detector
        self.stats = DetectionStatistics()
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(900, 600)
        self.root.configure(bg=THEME["bg"])
        self._current_panel = None
        self._setup_styles()
        self._setup_menu()
        self._setup_ui()
        self._show_panel("image")
        self.set_status("就绪 | 模型已加载")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=THEME["bg"])
        style.configure("TLabel", background=THEME["bg"], foreground=THEME["text_dark"])
        style.configure("TSidebar.TFrame", background=THEME["sidebar"])
        style.configure("TButton", font=("Microsoft YaHei", 9))
        style.configure("Accent.TButton", background=THEME["accent"],
                        foreground="white", font=("Microsoft YaHei", 10))
        style.map("Accent.TButton",
                  background=[("active", THEME["button_hover"])])

    def _setup_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # 文件菜单
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="设置", command=self._open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)

        # 视图菜单
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_command(label="图像检测", command=lambda: self._show_panel("image"))
        view_menu.add_command(label="摄像头检测", command=lambda: self._show_panel("camera"))
        view_menu.add_command(label="批量处理", command=lambda: self._show_panel("batch"))
        view_menu.add_command(label="检测统计", command=lambda: self._show_panel("history"))

        # 帮助菜单
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self._open_about)

    def _setup_ui(self):
        # 主容器
        self._main_frame = ttk.Frame(self.root)
        self._main_frame.pack(fill=tk.BOTH, expand=True)
        self._main_frame.columnconfigure(0, weight=1)
        self._main_frame.rowconfigure(1, weight=1)

        # 顶部标题栏
        header = tk.Frame(self._main_frame, bg=THEME["sidebar"], height=50)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        tk.Label(header, text="🌾 小麦病虫害识别系统",
                 bg=THEME["sidebar"], fg=THEME["text_light"],
                 font=("Microsoft YaHei", 16, "bold")).pack(side=tk.LEFT, padx=20, pady=8)

        # 导航按钮
        self._nav_frame = tk.Frame(header, bg=THEME["sidebar"])
        self._nav_frame.pack(side=tk.RIGHT, padx=10)

        nav_buttons = [
            ("📷 图像检测", "image"),
            ("🎥 摄像头", "camera"),
            ("📂 批量处理", "batch"),
            ("📊 统计", "history"),
        ]
        self._nav_btns = {}
        for text, mode in nav_buttons:
            btn = tk.Button(self._nav_frame, text=text,
                           bg=THEME["sidebar"], fg=THEME["text_light"],
                           font=("Microsoft YaHei", 9),
                           relief="flat", padx=10, cursor="hand2",
                           command=lambda m=mode: self._show_panel(m))
            btn.pack(side=tk.LEFT, padx=2)
            self._nav_btns[mode] = btn

        # 内容区
        self._content = ttk.Frame(self._main_frame)
        self._content.grid(row=1, column=0, sticky="nswe")
        self._content.columnconfigure(0, weight=1)
        self._content.rowconfigure(0, weight=1)

        # 状态栏
        self._status_bar = ttk.Label(self._main_frame, text="就绪",
                                     relief="sunken", anchor=tk.W,
                                     font=("Microsoft YaHei", 9),
                                     background=THEME["card"])
        self._status_bar.grid(row=2, column=0, sticky="ew")

    def _show_panel(self, mode: str):
        # 清除当前面板
        if self._current_panel:
            self._current_panel.destroy()

        # 更新导航按钮样式
        for m, btn in self._nav_btns.items():
            btn.config(bg=THEME["sidebar"])

        if mode in self._nav_btns:
            self._nav_btns[mode].config(bg=THEME["button_hover"])

        # 创建新面板
        status_cb = self.set_status
        if mode == "image":
            self._current_panel = ImageModePanel(
                self._content, self.detector, self.stats, status_cb)
        elif mode == "camera":
            self._current_panel = CameraModePanel(
                self._content, self.detector, self.stats, status_cb)
        elif mode == "batch":
            self._current_panel = BatchModePanel(
                self._content, self.detector, self.stats, status_cb)
        elif mode == "history":
            self._current_panel = HistoryPanel(
                self._content, self.detector, self.stats, status_cb)

        if self._current_panel:
            self._current_panel.grid(row=0, column=0, sticky="nswe")

    def _open_settings(self):
        dialog = SettingsDialog(self.root)
        self.root.wait_window(dialog)
        if dialog.result:
            self.set_status(f"设置已更新: 置信度={dialog.result['confidence']}")

    def _open_about(self):
        AboutDialog(self.root)

    def set_status(self, msg: str):
        self._status_bar.config(text=f"  {msg}")
        self.root.update_idletasks()

    def run(self):
        self.root.mainloop()
