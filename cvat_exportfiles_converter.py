import xml.etree.ElementTree as ET
import os

xml_file = "tracklet_labels.xml"
output_dir = "label_2"
os.makedirs(output_dir, exist_ok=True)

tree = ET.parse(xml_file)
root = tree.getroot()

for tracklet in root.findall(".//item"):
    obj_type = tracklet.findtext(".//objectType")
    h = tracklet.findtext(".//h")
    w = tracklet.findtext(".//w")
    l = tracklet.findtext(".//l")
    first_frame = tracklet.findtext(".//first_frame")

    if None in (obj_type, h, w, l, first_frame):
        continue  # 足りないデータをスルー

    h, w, l = float(h), float(w), float(l)
    first_frame = int(first_frame)

    # 各tracklet内。posesを取得
    for pose in tracklet.findall(".//poses/item"):
        tx = float(pose.findtext(".//tx"))
        ty = float(pose.findtext(".//ty"))
        tz = float(pose.findtext(".//tz"))
        ry = float(pose.findtext(".//ry", default="0"))

        # KITTIフォーマット: type truncated occluded alpha bbox xmin ymin xmax ymax dimensions location rotation_y
        line = f"{obj_type} 0 0 0 0 0 50 50 {h:.2f} {w:.2f} {l:.2f} {tx:.2f} {ty:.2f} {tz:.2f} {ry:.2f}\n"

        with open(os.path.join(output_dir, f"{first_frame:06d}.txt"), "a") as f:
            f.write(line)

print(f"Converted labels saved to: {output_dir}/")
