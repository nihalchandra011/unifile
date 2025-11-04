# backend/converters.py
import os, subprocess, mimetypes, pathlib, tempfile
from PIL import Image


OFFICE_EXT = {'.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp'}
IMG_EXT = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webp', '.bmp'}
TXT_EXT = {'.txt', '.md', '.rtf'}


async def convert_to_pdf(in_path: str, out_dir: str) -> str | None:
ext = pathlib.Path(in_path).suffix.lower()
base = pathlib.Path(in_path).stem
out_path = os.path.join(out_dir, f"{base}.pdf")


if ext in OFFICE_EXT:
# LibreOffice headless
cmd = ["soffice", "--headless", "--convert-to", "pdf", "--outdir", out_dir, in_path]
return out_path if subprocess.call(cmd) == 0 and os.path.exists(out_path) else None


if ext in IMG_EXT:
try:
with Image.open(in_path) as im:
im.load()
rgb = im.convert('RGB')
rgb.save(out_path, "PDF", resolution=300)
return out_path
except Exception:
return None


if ext == '.pdf':
# Normalize to ensure PDF/A-ish compatibility (optional): return as-is for speed
return in_path


if ext in TXT_EXT:
# quick text→pdf via LibreOffice
cmd = ["soffice", "--headless", "--convert-to", "pdf", "--outdir", out_dir, in_path]
return out_path if subprocess.call(cmd) == 0 and os.path.exists(out_path) else None


if ext in {'.one', '.onepkg'}:
# Placeholder: requires Graph API adapter or user exporting locally
return None


return None
