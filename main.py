from PIL import Image

Ina = {
    "Russia": "#8000ff",
    "United Kingdom": "#d75254",
    "Portugal": "#339933",
    "Spain": "#cccc33",
    "Netherlands": "#ff903a",
    "Belgium": "#6699cc",
    "United States": "#cc66cc",
    "Italy": "#00ff00",
    "Germany": "#804000",
    "Turkey": "#808080",
    "France": "#0000ff",
    "None": "#b9b9b9",
}

Colors = {
    # European / Northwest Eurasian
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
    # South Asian / Southern Eurasian
    "Gujarati": "#ea73ff",
    "Hindustani": "#e655ff",
    "Marathi": "#e02fff",
    "Northeast Indic": "#db0fff",
    "Nepali": "#af00ce",
    "Northwest Indic": "#cc00f0",
    "Sinhalese": "#88009f",
    "Indo South African": "#f700a0",
    "Indo-Caribbean": "#ff64c9",
    "Indo-Fijian": "#ff0fab",
    "Dardic": "#f69e80",
    "Burusho": "#ff73f4",
    "Nuristani": "#f79954",
    "Munda": "#86007c",
    "Dravidian": "#ff20ee",
    "Brahui": "#e800d7",
    "Moor": "#dd3b4c",
    "Vedda": "#ae00a2",
    "Adivasi": "#380035",
    "South Arabian": "#ff807a",
    "Romani": "#ffb7fa",
    "Domari": "#ff79f5",
    "Kholosi": "#ff59f2",
    # Southwest Eurasian
    "Arabian": "#ff781e",
    "Egyptian": "#ff8635",
    "Maghrebi": "#ff954f",
    "Levantine": "#ff9e5e",
    "Druze": "#ffaa71",
    "Maronite": "#ffb786",
    "Syriac": "#ffc199",
    "Melkite": "#ffd1b3",
    "Ashkenazi": "#fd6500",
    "Sephardi": "#e65b00",
    "Mizrahi": "#d05300",
    "Israeli": "#bf4d00",
    "Berber": "#ffd399",
    "Tuareg": "#ffcb84",
    "Siwa": "#ffe1b9",
    "Coptic": "#ffbf68",
    "Persian": "#ffae40",
    "Ossetian": "#ffa62d",
    "Parsi": "#ff9a11",
    "Western Iranic": "#df8a16",
    "Eastern Iranic": "#ee9216",
    "Caspian": "#cd7f16",
    "Turkic": "#f8ba76",
    "Kipchak": "#edc344",
    "Kouloughi": "#deb36f",
    "Caucasian": "#f59932",
    "Georgian": "#f48b17",
    "Armenian": "#d9770b",
    "Sudanese": "#ef9d5e",
    "Mauritanian": "#eb9652",
    # Eastern Eurasian
    "Japonic": "#fffbc4",
    "Korean": "#fff89b",
    "Mongolic": "#fff57d",
    "Tuvan": "#fff364",
    "Manchurian": "#efe143",
    "Turanid": "#d7c700",
    "Hazara": "#e1d000",
    "Northern Han": "#ffed20",
    "Southern Han": "#fbe800",
    "Southeast Asian Han": "#ffef2b",
    "Hui": "#ecda00",
    "Yakut": "#c8b900",
    "Chukotko": "#b9ab00",
    "Tungusic": "#ac9f00",
    "Ainu": "#a29600",
    "Bolgar": "#fbce46",
    "Volgaic": "#e6c537",
    "Samoyedic": "#dcc22d",
    "Vietic": "#f9ffc4",
    "Mon-Khmer": "#f4ff93",
    "Khasi": "#f0ff6f",
    "Formosan": "#e9ff20",
    "Philippine": "#ebff39",
    "Malayan": "#eeff55",
    "Tibetic": "#e1e41b",
    "Burmic": "#d9db1b",
    "Tai Kadai": "#e1fb00",
    "Hmong-Mien": "#9eb000",
    # African
    "Beja": "#a6ff39",
    "Cushitic": "#c7ff82",
    "Habesha": "#99d44c",
    "Omotic": "#9aff1e",
    "Beta Israel": "#88f700",
    "Chadic": "#a8ec53",
    "Nilotic": "#2d5100",
    "Maasai": "#396800",
    "Nubian": "#447b00",
    "Sudanic": "#4f8e00",
    "Western Nigritic": "#5eaa00",
    "Eastern Nigritic": "#68bd00",
    "Banda": "#3de80c",
    "Bantu": "#06ff1a",
    "Lemba": "#a5dc64",
    "Khoi": "#acffb3",
    "San": "#8eff97",
    "Hadze": "#68ff74",
    "Sandawe": "#53ff60",
    "Pygmy": "#72c48b",
    "Anglo-Caribbean": "#00f018",
    "Dutch-Caribbean": "#00d915",
    "Hispanic-Caribbean": "#00cc14",
    "Franco-Caribbean": "#00c113",
    "Gullah": "#00b512",
    "Maroon": "#00aa11",
    "Black American": "#009b10",
    "Krio": "#00770c",
    "Afro-Hispanic": "#15ff62",
    "Afro-Brazilian": "#00f750",
    "Swahili": "#007d28",
    "Zanj": "#00dd48",
    "Afro-Mascarene": "#096f24",
    # Amerindian
    "Eskimo-Aleut": "#ffaaaa",
    "Na-Dene": "#ff8888",
    "Plains": "#ff3e3e",
    "Meso": "#ff0d0d",
    "Mayan": "#e80000",
    "Chibchan": "#c60000",
    "Amazonian": "#9d0000",
    "Andean": "#f1525a",
    "Patagonian": "#ed252f",
    "Fuegian": "#ab3137",
    # Oceanian
    "Papuan": "#817334",
    "Aborigine": "#b4704b",
    "Negrito": "#9c6141",
    "Aslian": "#835136",
    "Andamanese": "#6d442e",
    "Micronesian": "#a79645",
    "Polynesian": "#bbaa59",
    "Moluccan": "#cea48c",
    "Melanesian": "#be8465",
    # Multiracial
    "African Creole": "#97aa95",
    "Asian Creole": "#b8b98e",
    "Pacific Creole": "#aba894",
    "Louisiana Creole": "#5ca771",
    "Castizo": "#afbed5",
    "Northern Mestizo": "#879b99",
    "Southern Mestizo": "#9ca2a7",
    "Paraguayan Mestizo": "#7e7871",
    "Fiegian Mestizo": "#8a6f6c",
    "Metis": "#7f9793",
    "Dane-Inuit": "#bec1c5",
    # "Hispano-Mulatto": "#536258",
    # "Franco-Mulatto": "#46534a",
    # "Anglo-Mulatto": "#555555",
    "Pardo": "#70877f",
    "Montubio": "#78a494",
    "Papiamento": "#4e7a61",
    "Hispano-Zambo": "#947070",
    "Anglo-Zambo": "#886666",
    "Dougla": "#927283",
    "Malagasy": "#849146",
    "Other": "#3c463f",
    # Map
    # "Country Border": "#0f1719",
    "": "#",
    }

def filter_image(input_path, output_path, allowed_colors):
    # Open the image
    image = Image.open(input_path).convert("RGBA")
    pixels = image.load()
    width, height = image.size
    
    # Convert allowed colors to a set for faster lookup
    allowed_hex = set(color.lower() for color in allowed_colors.values())
    
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            hex_color = f"#{r:02x}{g:02x}{b:02x}".lower()
            
            # If color is not in the allowed list, make it transparent
            if hex_color not in allowed_hex:
                pixels[x, y] = (0, 0, 0, 0)  # Transparent pixel
    
    # Save the new image
    image.save(output_path, "PNG")

filter_image("ina.png", "ina1.png", Ina)



# # Open the image
# image = Image.open("map.png")

# # Convert image to RGB mode (in case it's not)
# image = image.convert("RGB")

# # Get all pixels as a list
# pixels = list(image.getdata())

# # Convert pixels to hex
# hex_pixels = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in pixels]

# # Save hex pixels to a text file
# with open("hex_pixels.txt", "w") as f:
#     for hex_color in hex_pixels:
#         f.write(f"{hex_color}\n")

# # Get unique colors
# # unique_colors = list(set(pixels))

# # Get unique colors and convert them to hex
# unique_hex_colors = list(set(f"#{r:02x}{g:02x}{b:02x}" for r, g, b in pixels))


# # Print the unique colors
# print(unique_hex_colors)
