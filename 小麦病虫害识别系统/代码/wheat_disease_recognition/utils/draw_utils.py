import cv2
import numpy as np

from config import CLASS_NAMES, CLASS_COLORS


def draw_detection_boxes(image: np.ndarray,
                          boxes: list,
                          class_ids: list,
                          confidences: list,
                          font_scale: float = 0.6) -> np.ndarray:
    """在图像上绘制检测框和标签"""
    result = image.copy()
    for box, cls_id, conf in zip(boxes, class_ids, confidences):
        x1, y1, x2, y2 = map(int, box)
        color = CLASS_COLORS.get(cls_id, (255, 255, 255))
        label = f"{CLASS_NAMES.get(cls_id, '未知')} {conf:.1%}"

        # 绘制检测框
        cv2.rectangle(result, (x1, y1), (x2, y2), color, 2)

        # 绘制标签背景
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX,
                                       font_scale, 2)
        cv2.rectangle(result, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)

        # 绘制标签文字
        cv2.putText(result, label, (x1 + 2, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2)

    return result


def create_legend_image(class_counts: dict, width: int = 200,
                         height: int = 200) -> np.ndarray:
    """创建图例图像（用于在GUI中显示类别分布）"""
    legend = np.ones((height, width, 3), dtype=np.uint8) * 255
    y = 10
    for cls_id, name in CLASS_NAMES.items():
        count = class_counts.get(name, 0)
        color = CLASS_COLORS.get(cls_id, (255, 255, 255))
        cv2.rectangle(legend, (10, y), (30, y + 12), color, -1)
        cv2.putText(legend, f"{name}: {count}", (35, y + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 50, 50), 1)
        y += 20
    return legend


def add_status_overlay(image: np.ndarray, text: str,
                       position: str = "topleft") -> np.ndarray:
    """在图像上叠加状态文字"""
    result = image.copy()
    h, w = result.shape[:2]

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    (tw, th), _ = cv2.getTextSize(text, font, font_scale, thickness)

    if position == "topleft":
        x, y = 5, th + 5
    elif position == "topright":
        x, y = w - tw - 5, th + 5
    elif position == "bottomleft":
        x, y = 5, h - 5
    elif position == "bottomright":
        x, y = w - tw - 5, h - 5
    else:
        x, y = 5, th + 5

    cv2.putText(result, text, (x, y), font, font_scale, (255, 255, 255), thickness)
    return result
