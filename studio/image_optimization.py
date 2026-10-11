"""Create compact web images while preserving transparency and originals."""
from io import BytesIO
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from PIL import Image, ImageOps


def optimize_image(source, max_size=1920):
    if PurePosixPath(source.name).suffix.lower() == '.svg':
        return None
    source.open('rb')
    try:
        raw = source.read()
        with Image.open(BytesIO(raw)) as original:
            if getattr(original, 'is_animated', False):
                return None
            image = ImageOps.exif_transpose(original)
            resized = max(image.size) > max_size
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            image = image.convert('RGBA' if 'A' in image.getbands() or 'transparency' in image.info else 'RGB')
            output = BytesIO()
            image.save(output, 'WEBP', quality=82, method=6)
        if not resized and len(output.getvalue()) >= len(raw):
            return None
        stem = PurePosixPath(source.name).stem
        return ContentFile(output.getvalue(), name=stem + '-web.webp')
    finally:
        source.seek(0)
