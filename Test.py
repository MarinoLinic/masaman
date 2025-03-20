import cv2
import numpy as np
from PIL import Image
from shapely.geometry import Polygon, mapping
import geojson

# Define colors dictionary
Colors = {
    "Franco": "#008db5",
    "Iberian": "#00a7d7",
    "Italic": "#008695",
    "Sardinian": "#9c97ff",
    "Rhaetian": "#00a0b3",
    "Romanian": "#00717d",
    "Canarian": "#4b0ae7",
    "Criollo": "#9dc5ff",
    "Hispano-Caribbean (West)": "#6ba5ff",
    "Luso-Brazilian": "#62a0ff",
    "West Slavic": "#9de9ff",
    "East Slavic": "#6cdeff",
    "South Slavic": "#84e3ff",
    "Baltic": "#007293",
    "Anglo": "#62efff",
    "Germanic": "#00daf2",
    "Scandinavian": "#00c5db",
    "Afrikaner": "#00b8cc",
    "Mormon": "#9df5ff",
    "Celtic": "#034b9f",
    "Falklander": "#0a99cf",
    "Albanian": "#3184ff",
    "Greek": "#3c31ff",
    "Gagauz": "#0c00f0",
    "Maltese": "#0b00ce",
    "Basque": "#0900a4",
    "Hungarian": "#7c78da",
    "Finnic": "#070095",
    "Sami": "#4a43d4",
}

# Convert hex color to BGR (OpenCV format)
def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (4, 2, 0))  # Convert to (B, G, R)

# Load the image
image = cv2.imread("old-map.png")

# GeoJSON and SVG storage
geojson_features = []
svg_paths = []

# Image dimensions
height, width, _ = image.shape

# Iterate over each color in dictionary
for region_name, hex_color in Colors.items():
    bgr_color = hex_to_bgr(hex_color)

    # Create mask for the specific color
    mask = cv2.inRange(image, np.array(bgr_color), np.array(bgr_color))

    # Find contours (polygons)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if len(contour) >= 3:  # Ignore small artifacts
            polygon = [(int(pt[0][0]), int(pt[0][1])) for pt in contour]
            shapely_polygon = Polygon(polygon)

            # Save to GeoJSON
            geojson_features.append(geojson.Feature(
                geometry=mapping(shapely_polygon),
                properties={"name": region_name, "color": hex_color}
            ))

            # Convert to SVG path
            path_data = "M " + " L ".join(f"{x},{y}" for x, y in polygon) + " Z"
            svg_paths.append(f'<path d="{path_data}" fill="{hex_color}" stroke="black" stroke-width="1" data-name="{region_name}"/>')

# Create GeoJSON FeatureCollection
# geojson_data = geojson.FeatureCollection(geojson_features)
# with open("map_data.geojson", "w") as f:
#     geojson.dump(geojson_data, f)
# print("GeoJSON file saved as map_data.geojson")

# Save SVG
svg_content = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">\n' + "\n".join(svg_paths) + "\n</svg>"
with open("map_data.svg", "w") as f:
    f.write(svg_content)
print("SVG file saved as map_data.svg")
