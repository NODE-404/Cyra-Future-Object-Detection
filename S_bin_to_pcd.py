#bin_to_pcd.py
#Simple

import numpy as np
import open3d as o3d
import sys

# 例: python bin_to_pcd.py 000000.bin 000000.pcd
bin_path = sys.argv[1]
pcd_path = sys.argv[2]

# KITTIの.binは float32 で x, y, z, intensity が連続
points = np.fromfile(bin_path, dtype=np.float32).reshape(-1, 4)

# Open3DでPointCloud作成
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points[:, :3])
pcd.colors = o3d.utility.Vector3dVector(np.tile(points[:, 3:4], (1, 3)))  # 強度→色可視化

o3d.io.write_point_cloud(pcd_path, pcd)
print(f"Saved: {pcd_path}")
