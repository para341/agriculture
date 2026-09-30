import os
import csv
from typing import List

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from core.detector import DetectionResult
from config import CLASS_NAMES, EXPORTS_DIR


class DetectionStatistics:
    """检测结果统计模块"""

    def __init__(self):
        self.history: List[DetectionResult] = []
        self._class_counts = {name: 0 for name in CLASS_NAMES.values()}

    def add_result(self, result: DetectionResult):
        """添加一次检测结果到统计"""
        self.history.append(result)
        for cls_name in result.class_names:
            if cls_name in self._class_counts:
                self._class_counts[cls_name] += 1

    def get_class_distribution(self) -> dict:
        """获取各类别检测数量分布"""
        return dict(self._class_counts)

    def get_confidence_stats(self) -> dict:
        """获取置信度统计"""
        all_conf = []
        for res in self.history:
            all_conf.extend(res.confidences)
        if not all_conf:
            return {"min": 0, "max": 0, "avg": 0, "count": 0}
        return {
            "min": round(min(all_conf), 3),
            "max": round(max(all_conf), 3),
            "avg": round(sum(all_conf) / len(all_conf), 3),
            "count": len(all_conf),
        }

    def export_csv(self, filepath: str = None) -> str:
        """导出检测结果到CSV文件"""
        if filepath is None:
            os.makedirs(EXPORTS_DIR, exist_ok=True)
            import time
            filepath = os.path.join(EXPORTS_DIR, f"detection_report_{int(time.time())}.csv")

        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["序号", "类别", "置信度", "x1", "y1", "x2", "y2"])
            idx = 1
            for res in self.history:
                for cls_name, conf, box in zip(res.class_names, res.confidences, res.boxes):
                    x1, y1, x2, y2 = map(lambda v: round(v, 1), box)
                    writer.writerow([idx, cls_name, f"{conf:.2%}", x1, y1, x2, y2])
                    idx += 1
        return filepath

    def plot_distribution(self, save_path: str = None) -> str:
        """绘制类别分布柱状图"""
        os.makedirs(EXPORTS_DIR, exist_ok=True)
        names = list(self._class_counts.keys())
        counts = list(self._class_counts.values())

        plt.figure(figsize=(10, 6))
        colors = ['#e74c3c', '#2ecc71', '#f39c12', '#f1c40f', '#3498db']
        bars = plt.bar(names, counts, color=colors[:len(names)])
        plt.title("检测类别分布统计", fontsize=14)
        plt.xlabel("病害类别", fontsize=12)
        plt.ylabel("检测数量", fontsize=12)
        plt.xticks(rotation=15)

        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                     str(count), ha='center', va='bottom')

        if save_path is None:
            import time
            save_path = os.path.join(EXPORTS_DIR, f"distribution_{int(time.time())}.png")
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
        return save_path

    def clear(self):
        """清空统计"""
        self.history.clear()
        self._class_counts = {name: 0 for name in CLASS_NAMES.values()}
