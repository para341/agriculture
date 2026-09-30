import cv2
import numpy as np


class Preprocessor:
    """图像预处理模块：提供多种传统图像处理方法"""

    @staticmethod
    def resize_with_aspect_ratio(image: np.ndarray, target_size: int = 640) -> np.ndarray:
        """保持宽高比的resize，不足部分用黑边填充"""
        h, w = image.shape[:2]
        scale = target_size / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # 填充黑边到目标尺寸
        canvas = np.zeros((target_size, target_size, 3), dtype=np.uint8)
        x_offset = (target_size - new_w) // 2
        y_offset = (target_size - new_h) // 2
        canvas[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized
        return canvas

    @staticmethod
    def apply_clahe(image: np.ndarray, clip_limit: float = 2.0,
                    grid_size: tuple = (8, 8)) -> np.ndarray:
        """
        CLAHE直方图均衡化
        增强局部对比度，使病害区域特征更明显
        """
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
        l_eq = clahe.apply(l)
        lab_eq = cv2.merge([l_eq, a, b])
        return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

    @staticmethod
    def gaussian_blur(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """
        高斯滤波去噪
        平滑图像，减少传感器噪声对检测的影响
        """
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    @staticmethod
    def sharpen(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
        """
        拉普拉斯锐化
        增强病害边缘纹理，使病害边界更清晰
        """
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=np.float32)
        kernel *= strength
        return cv2.filter2D(image, -1, kernel)

    @staticmethod
    def adjust_brightness_contrast(image: np.ndarray, alpha: float = 1.2,
                                   beta: int = 10) -> np.ndarray:
        """调整亮度和对比度"""
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    @staticmethod
    def apply_canny(image: np.ndarray, low: int = 50, high: int = 150) -> np.ndarray:
        """Canny边缘检测，用于展示病害区域边缘"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, low, high)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def gamma_correction(image: np.ndarray, gamma: float = 1.5) -> np.ndarray:
        """
        伽马校正（幂次变换）
        调整图像亮度，暗部细节增强，用于改善田间光照不均
        """
        inv_gamma = 1.0 / gamma
        table = np.array([(i / 255.0) ** inv_gamma * 255
                          for i in range(256)], dtype=np.uint8)
        return cv2.LUT(image, table)

    @staticmethod
    def morphology_open(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """
        形态学开运算（先腐蚀后膨胀）
        去除检测结果中的小白点噪声，平滑轮廓
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    @staticmethod
    def morphology_close(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """
        形态学闭运算（先膨胀后腐蚀）
        填充目标内部的小孔洞，连接邻近区域
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

    @staticmethod
    def fourier_spectrum(image: np.ndarray) -> np.ndarray:
        """
        傅里叶频谱图
        将图像从空间域变换到频率域，用于频率域分析
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        f = np.fft.fft2(gray.astype(np.float32))
        fshift = np.fft.fftshift(f)
        magnitude = np.log(np.abs(fshift) + 1)
        magnitude = (magnitude / magnitude.max() * 255).astype(np.uint8)
        return cv2.cvtColor(magnitude, cv2.COLOR_GRAY2BGR)

    def preprocess(self, image: np.ndarray, options: dict = None) -> np.ndarray:
        """
        根据选项应用预处理流程
        options: {"clahe": bool, "gaussian_blur": bool, "sharpen": bool,
                  "canny": bool, "gamma": bool, "morphology": bool}
        """
        if options is None:
            options = {}
        result = image.copy()

        if options.get("gaussian_blur"):
            result = self.gaussian_blur(result)
        if options.get("clahe"):
            result = self.apply_clahe(result)
        if options.get("sharpen"):
            result = self.sharpen(result)
        if options.get("canny"):
            result = self.apply_canny(result)
        if options.get("gamma"):
            result = self.gamma_correction(result)
        if options.get("morphology"):
            result = self.morphology_open(result)

        return result
