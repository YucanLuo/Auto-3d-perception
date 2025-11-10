import os
import sys

# === 确保可以导入 src 包 ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data.s3dis_dataset import S3DISDataset
from src.utils.preprocess import preprocess_points
from src.utils.visualization import save_point_cloud_matplotlib


def main():
    dataset = S3DISDataset(
        root_dir="/workspace/data/S3DIS",
        areas=(1,),
        num_points=4096
    )

    print(f"[S3DISDataset] Found {len(dataset)} samples.")
    points, labels = dataset[0]
    points_np = points.numpy()
    labels_np = labels.numpy()

    # 预处理
    points_proc = preprocess_points(points_np, use_color=True)

    # 保存 Matplotlib 可视化结果
    save_point_cloud_matplotlib(
        points_proc,
        labels=labels_np,
        save_path="results/visual_samples/s3dis_area1_sample0_matplotlib.png"
    )


if __name__ == "__main__":
    main()
