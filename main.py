from PIL import Image

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
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    "": "#",
    }

# Open the image
image = Image.open("map.png")

# Convert image to RGB mode (in case it's not)
image = image.convert("RGB")

# Get all pixels as a list
pixels = list(image.getdata())

# Convert pixels to hex
hex_pixels = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in pixels]

# Save hex pixels to a text file
with open("hex_pixels.txt", "w") as f:
    for hex_color in hex_pixels:
        f.write(f"{hex_color}\n")

# Get unique colors
# unique_colors = list(set(pixels))

# Get unique colors and convert them to hex
unique_hex_colors = list(set(f"#{r:02x}{g:02x}{b:02x}" for r, g, b in pixels))


# Print the unique colors
print(unique_hex_colors)
