"""Prepare the Masaman assets, export a portable chart, or run a local preview."""

import argparse
import base64
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import re
from threading import Timer

ROOT = Path(__file__).resolve().parent
IMAGE_FIELDS = ("image", "key", "original")
COLOR = re.compile(r"#[0-9a-fA-F]{6}")


def prepare(masked, destination):
    from PIL import Image, ImageDraw

    with Image.open(ROOT / "old-map.png") as original, Image.open(masked) as image:
        if original.size != (13226, 6176) or image.size != (11775, 6147) or image.mode != "RGBA":
            raise ValueError("Expected the original PNG and its Photo Tools background-removal output.")
        # Source credit begins at x=11734, y=6017. The map ends well to its left
        # on these rows. The unchanged original and the viewer both carry attribution.
        ImageDraw.Draw(image).rectangle((11734 - 26, 6017 - 29, image.width, image.height), fill=(0, 0, 0, 0))
        image.save(destination / "masaman-map.png")
        original.crop((11893, 149, 13067, 2049)).save(destination / "masaman-key.png", optimize=True)


def data_url(path):
    mime = mimetypes.guess_type(path.name)[0]
    if not mime or not mime.startswith("image/"):
        raise ValueError(f"Expected an image file: {path}")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def export(definition, output):
    config = json.loads(definition.read_text(encoding="utf-8-sig"))
    if not config.get("title") or not config.get("image"):
        raise ValueError("The chart definition needs a title and image.")
    for group in config.get("legend", []):
        for entry in group["entries"]:
            colors = [entry["color"], *entry.get("aliases", [])]
            if not entry.get("label") or not all(COLOR.fullmatch(color) for color in colors):
                raise ValueError(f"Expected a label and six-digit hex colors for {entry!r}")

    if config.get("original"):
        config["originalName"] = Path(config["original"]).name
    for field in IMAGE_FIELDS:
        if config.get(field):
            config[field] = data_url(definition.parent / config[field])
    inline = json.dumps(config, ensure_ascii=False).replace("<", "\\u003c")
    html = (ROOT / "index.html").read_text(encoding="utf-8-sig")
    html = html.replace('href="favicon.svg"', f'href="{data_url(ROOT / "favicon.svg")}"')
    css = (ROOT / "viewer.css").read_text(encoding="utf-8-sig")
    html = html.replace('<link rel="stylesheet" href="viewer.css">', f"<style>\n{css}</style>")
    script = (ROOT / "viewer.js").read_text(encoding="utf-8-sig")
    html = html.replace('<script src="viewer.js" defer></script>', f"<script>\n{script}</script>")
    html = html.replace(
        '<script id="chart-config" type="application/json"></script>',
        f'<script id="chart-config" type="application/json">{inline}</script>',
    )
    with output.open("x", encoding="utf-8") as stream:
        stream.write(html)


def preview(port, seconds):
    if seconds <= 0:
        raise ValueError("Preview lifetime must be positive.")
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        timer = Timer(seconds, server.shutdown)
        timer.daemon = True
        timer.start()
        print(f"http://127.0.0.1:{server.server_port}/ (closes after {seconds} seconds)", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            timer.cancel()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    assets = commands.add_parser("prepare", help="Build the original map and key crops")
    assets.add_argument("masked", type=Path, help="PNG produced by Photo Tools")
    assets.add_argument("--output-dir", type=Path, default=ROOT / "charts")
    portable = commands.add_parser("export", help="Export a self-contained HTML file")
    portable.add_argument("definition", type=Path)
    portable.add_argument("output", type=Path)
    serve = commands.add_parser("preview", help="Serve the viewer locally for a fixed duration")
    serve.add_argument("--port", type=int, default=4173)
    serve.add_argument("--seconds", type=int, default=7200)
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.masked, args.output_dir)
    elif args.command == "export":
        export(args.definition, args.output)
    else:
        preview(args.port, args.seconds)


if __name__ == "__main__":
    main()
