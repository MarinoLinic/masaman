import cv2
import numpy as np
import potrace
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

# Load the image
image_path = "filtered_map.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Apply threshold to create a binary image
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

# Convert to potrace bitmap format
bitmap = potrace.Bitmap(binary_image)

# Trace the bitmap
path = bitmap.trace()

# Create SVG structure
svg = Element("svg", xmlns="http://www.w3.org/2000/svg", version="1.1")
svg.set("viewBox", f"0 0 {binary_image.shape[1]} {binary_image.shape[0]}")

# Add paths
for curve in path:
    d = "M {} {} ".format(curve.start_point.x, curve.start_point.y)
    for segment in curve:
        if segment.is_corner:
            d += "L {} {} ".format(segment.c.x, segment.c.y)
            d += "L {} {} ".format(segment.end_point.x, segment.end_point.y)
        else:
            d += "C {} {}, {} {}, {} {} ".format(segment.c1.x, segment.c1.y,
                                                 segment.c2.x, segment.c2.y,
                                                 segment.end_point.x, segment.end_point.y)
    path_element = SubElement(svg, "path", d=d, fill="black")

# Beautify and save SVG
xml_str = xml.dom.minidom.parseString(tostring(svg)).toprettyxml()
with open("filtered_map.svg", "w", encoding="utf-8") as f:
    f.write(xml_str)

print("Conversion complete: filtered_map.svg")
