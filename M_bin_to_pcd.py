import numpy as np
import open3d as o3d
import os
import sys


if len(sys.argv) < 3:
    print("Usage: python bin_to_pcd.py <input_bin_dir> <output_pcd_dir>")
    sys.exit(1)
bin_dir = sys.argv[1]
pcd_dir = sys.argv[2]

# 出力先作成
os.makedirs(pcd_dir, exist_ok=True)

# ディレクトリ内の .bin ファイルを全取得の後にソート
bin_files = sorted([f for f in os.listdir(bin_dir) if f.endswith(".bin")])

if not bin_files:
    print("No .bin files found in the input directory.")
    sys.exit(1)

for f in bin_files:
    bin_path = os.path.join(bin_dir, f)
    pcd_filename = os.path.splitext(f)[0] + ".pcd"
    pcd_path = os.path.join(pcd_dir, pcd_filename)

    # KITTI形式: x, y, z, intensity（float32）
    points = np.fromfile(bin_path, dtype=np.float32).reshape(-1, 4)

    # Open3D PointCloud作成
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])

    # intensity をグレースケール感で可視化
    intensities = points[:, 3:4]
    norm_intensity = (intensities - intensities.min()) / (intensities.ptp() + 1e-8)
    pcd.colors = o3d.utility.Vector3dVector(np.tile(norm_intensity, (1, 3)))
    o3d.io.write_point_cloud(pcd_path, pcd)
    print(f"Saved: {pcd_path}")

print("All .bin files have been converted to .pcd.")
