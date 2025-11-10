import os
import numpy as np
import open3d as o3d
import matplotlib
matplotlib.use("Agg")  # 无GUI环境使用
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


# 固定一个简单的label颜色表(13类)
LABEL_COLORS = np.array([
    [0, 0, 255],      # 0 ceiling - blue
    [0, 255, 0],      # 1 floor - green
    [255, 0, 0],      # 2 wall - red
    [255, 255, 0],    # 3 beam - yellow
    [255, 0, 255],    # 4 column - magenta
    [0, 255, 255],    # 5 window - cyan
    [100, 100, 255],  # 6 door
    [200, 200, 200],  # 7 table
    [150, 75, 0],     # 8 chair
    [255, 165, 0],    # 9 sofa
    [128, 0, 128],    # 10 bookcase
    [0, 128, 128],    # 11 board
    [128, 128, 128],  # 12 clutter
], dtype=np.float32) / 255.0


def points_to_pcd(points: np.ndarray,
                  labels: np.ndarray = None,
                  use_rgb: bool = True) -> o3d.geometry.PointCloud:
    """
    将点云+颜色/标签转换为 Open3D 的 PointCloud 对象
    points: (N,6) -> xyzrgb(已归一化或未归一化均可)
    labels: (N,) or None
    """
    assert points.ndim == 2
    xyz = points[:, :3]

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)

    if use_rgb and points.shape[1] >= 6:
        # 使用归一化后的 RGB
        colors = points[:, 3:6].copy()
        # 若范围不是[0,1]，则做一次clip
        colors = np.clip(colors, 0.0, 1.0)
        pcd.colors = o3d.utility.Vector3dVector(colors)
    elif labels is not None:
        # 用 label 上色
        colors = LABEL_COLORS[np.clip(labels, 0, LABEL_COLORS.shape[0]-1)]
        pcd.colors = o3d.utility.Vector3dVector(colors)
    else:
        # 默认给个常数色
        colors = np.ones_like(xyz) * 0.5
        pcd.colors = o3d.utility.Vector3dVector(colors)

    return pcd


def show_point_cloud(points, labels=None, use_rgb=True):
    """
    交互式可视化（需要有图形界面支持）
    """
    pcd = points_to_pcd(points, labels, use_rgb=use_rgb)
    o3d.visualization.draw_geometries([pcd])


def save_point_cloud_image(points,
                           labels=None,
                           use_rgb=True,
                           save_path="results/visual_samples/sample.png",
                           width=800,
                           height=600):
    """
    优先用 Open3D 离屏渲染；如果当前环境不支持，则给出提示。
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    pcd = points_to_pcd(points, labels, use_rgb=use_rgb)

    vis = o3d.visualization.Visualizer()
    ok = vis.create_window(visible=False, width=width, height=height)
    if not ok:
        print("[Visualization] WARN: Failed to create Open3D window in this environment. "
              "Skipping image save (this does NOT affect your dataset or pipeline).")
        vis.destroy_window()
        return

    vis.add_geometry(pcd)
    opt = vis.get_render_option()
    if opt is not None:
        opt.background_color = np.array([1, 1, 1])

    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    vis.capture_screen_image(save_path)
    vis.destroy_window()

    print(f"[Visualization] Saved point cloud image to: {save_path}")

def save_point_cloud_matplotlib(points,
                                labels=None,
                                save_path="results/visual_samples/sample_matplotlib.png",
                                num_points=4096):
    """
    使用 matplotlib 在无头环境下保存点云截图。
    不依赖 OpenGL / Open3D 的窗口，因此在 Docker 里非常稳定。
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    pts = points
    if pts.shape[0] > num_points:
        idx = np.random.choice(pts.shape[0], num_points, replace=False)
        pts = pts[idx]
        if labels is not None:
            labels = labels[idx]

    x, y, z = pts[:, 0], pts[:, 1], pts[:, 2]

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')

    if labels is not None:
        sc = ax.scatter(x, y, z, c=labels, s=1, cmap='tab20')
    else:
        sc = ax.scatter(x, y, z, s=1)

    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close(fig)

    print(f"[Visualization] Saved matplotlib point cloud image to: {save_path}")
