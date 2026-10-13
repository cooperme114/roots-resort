#!/usr/bin/env python3
"""Build a single self-contained HTML file for Google Sites Embed code."""
import base64
import json
import mimetypes
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / "index.html").read_text(encoding="utf-8")
assets = {}
for path in (root / "sprites").rglob("*"):
    if not path.is_file() or path.suffix.lower() not in (".png", ".gif", ".jpg", ".jpeg", ".webp", ".svg"):
        continue
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    assets[path.relative_to(root).as_posix()] = "data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode("ascii")

# Resolve both dynamically constructed sprite filenames and URL-encoded spaces.
bootstrap = """
const EMBEDDED_SPRITES = __ASSETS__;
function embedAsset(path) {
  const key = decodeURIComponent(String(path)).replace(/^\\.\\//, '').split('?')[0];
  return EMBEDDED_SPRITES[key] || path;
}
function EmbeddedImage() {
  const im = new Image();
  const descriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'src');
  Object.defineProperty(im, 'src', {
    configurable: true,
    get() { return descriptor.get.call(im); },
    set(value) { descriptor.set.call(im, embedAsset(value)); }
  });
  return im;
}
""".replace("__ASSETS__", json.dumps(assets, separators=(",", ":")))
if "<script>" not in source:
    raise RuntimeError("Could not find the game's script tag")
source = source.replace("<script>", "<script>\\n" + bootstrap + "\\n", 1)
source = source.replace("new Image()", "new EmbeddedImage()")
# The helper itself must create a native image, not call itself recursively.
source = source.replace("function EmbeddedImage() {\\n  const im = new EmbeddedImage();", "function EmbeddedImage() {\\n  const im = new Image();")
# Shop previews are created using HTML strings rather than Image.src setters.
source = source.replace("'<div class=\"shop-preview\"><img src=\"'+src+'", "'<div class=\"shop-preview\"><img src=\"'+embedAsset(src)+'")
output = root / "google-sites" / "embed-code.txt"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(source, encoding="utf-8")
print(f"Built {output} ({output.stat().st_size:,} bytes; {len(assets)} sprite assets)")
