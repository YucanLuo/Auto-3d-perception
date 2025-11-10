import numpy as np
import torch


def normalize_coordinates(points: np.ndarray, method: str = "room"):
    """
    对坐标进行归一化:
    - method='room': 减去中心, 再按最大范围缩放到 [-1,1]
    points: (N, 3) or (N, 6) numpy 数组
    """
    assert points.ndim == 2
    coords = points[:, :3]

    # 中心化
    center = (coords.max(axis=0) + coords.min(axis=0)) / 2.0
    coords_centered = coords - center

    # 缩放到 [-1,1]
    scale = np.max(np.linalg.norm(coords_centered, axis=1))
    if scale < 1e-6:
        scale = 1.0
    coords_norm = coords_centered / scale

    out = points.copy()
    out[:, :3] = coords_norm
    return out


def normalize_colors(points: np.ndarray):
    """
    将 RGB 从 [0,255] 归一化到 [0,1]（如果还没归一化的话）
    """
    out = points.copy()
    if out.shape[1] >= 6:
        rgb = out[:, 3:6]
        if rgb.max() > 1.5:  # 说明还是0-255
            out[:, 3:6] = rgb / 255.0
    return out


def preprocess_points(points: np.ndarray, use_color: bool = True):
    """
    综合预处理:
    1) 坐标中心化+归一化
    2) 颜色归一化到[0,1]
    返回 numpy 数组
    """
    pts = normalize_coordinates(points)
    if use_color:
        pts = normalize_colors(pts)
    return pts


def to_tensor(points: np.ndarray, labels: np.ndarray):
    """
    转成 PyTorch Tensor, 常用于最终喂模型
    """
    pts_t = torch.from_numpy(points).float()
    lbl_t = torch.from_numpy(labels).long()
    return pts_t, lbl_t


if __name__ == "__main__":
    # 简单自测
    dummy = np.random.rand(1000, 6) * 10.0
    out = preprocess_points(dummy)
    print("Input range:", dummy[:, :3].min(), dummy[:, :3].max())
    print("Output range:", out[:, :3].min(), out[:, :3].max())
