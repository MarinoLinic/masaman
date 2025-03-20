import cv2
import numpy as np
from PIL import Image
from shapely.geometry import Polygon, mapping
import geojson

# Load the color dictionary
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
    "Sami": "#4a43d4"
    }

# Convert hex colors to BGR for OpenCV
def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (4, 2, 0))  # Convert to (B, G, R)

# Load the image
image = cv2.imread("map.png")

# Convert to grayscale (optional, for debugging)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Prepare GeoJSON structure
geojson_features = []

for region_name, hex_color in Colors.items():
    bgr_color = hex_to_bgr(hex_color)

    # Create mask for this color
    mask = cv2.inRange(image, np.array(bgr_color), np.array(bgr_color))

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Convert contours to polygons
    for contour in contours:
        if len(contour) >= 3:  # Only consider valid polygons
            polygon = [(int(pt[0][0]), int(pt[0][1])) for pt in contour]
            shapely_polygon = Polygon(polygon)

            # Add to GeoJSON
            geojson_features.append(geojson.Feature(
                geometry=mapping(shapely_polygon),
                properties={"name": region_name, "color": hex_color}
            ))

# Create GeoJSON FeatureCollection
geojson_data = geojson.FeatureCollection(geojson_features)

# Save to file
with open("map_data.geojson", "w") as f:
    geojson.dump(geojson_data, f)

print("GeoJSON file saved as map_data.geojson")
