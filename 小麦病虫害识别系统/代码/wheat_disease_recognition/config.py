import os

# 模型路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "de_ide.pt")

# 类别名称
CLASS_NAMES = {0: '叶锈病', 1: '健康', 2: '散黑穗病', 3: '黄锈病', 4: '秆锈病'}

# 类别对应的BGR颜色（用于OpenCV绘制）
CLASS_COLORS = {
    0: (0, 0, 255),      # 叶锈病 - 红色
    1: (0, 200, 0),      # 健康 - 绿色
    2: (0, 165, 255),    # 散黑穗病 - 橙色
    3: (0, 255, 255),    # 黄锈病 - 黄色
    4: (255, 0, 0),      # 秆锈病 - 蓝色
}

# UI配置
WINDOW_TITLE = "小麦病虫害识别系统 v1.0"
WINDOW_SIZE = "1200x800"
THUMBNAIL_SIZE = (640, 480)
CAMERA_INDEX = 0
FPS_UPDATE_INTERVAL = 500  # ms

# 检测阈值
CONFIDENCE_THRESHOLD = 0.25
IOU_THRESHOLD = 0.45

# 预处理选项
PREPROCESS_OPTIONS = {
    "clahe": {"label": "CLAHE直方图均衡化", "default": False},
    "gaussian_blur": {"label": "高斯滤波去噪", "default": False},
    "sharpen": {"label": "拉普拉斯锐化", "default": False},
    "canny": {"label": "Canny边缘检测", "default": False},
    "gamma": {"label": "伽马校正(幂次变换)", "default": False},
    "morphology": {"label": "形态学开运算去噪", "default": False},
}

# 结果保存路径
RESULTS_DIR = os.path.join(BASE_DIR, "results")
DETECTIONS_DIR = os.path.join(RESULTS_DIR, "detections")
EXPORTS_DIR = os.path.join(RESULTS_DIR, "exports")

# 支持的图片格式
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

# 绿色农业主题配色
THEME = {
    "bg": "#F0F5E8",
    "sidebar": "#2E7D32",
    "accent": "#4CAF50",
    "text_light": "#FFFFFF",
    "text_dark": "#333333",
    "card": "#FFFFFF",
    "border": "#C8E6C9",
    "button_hover": "#388E3C",
}
