from io import BytesIO
import warnings
from PIL import Image, ImageEnhance, ImageOps, UnidentifiedImageError

MAX_IMAGE_BYTES = 10 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 25_000_000

def enhance(image_bytes) -> bytes:
    if not image_bytes or len(image_bytes) > MAX_IMAGE_BYTES:
        raise ValueError("Upload a JPG, PNG or WebP image smaller than 10 MB.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(image_bytes)) as source:
                if source.format not in {"JPEG", "PNG", "WEBP"}:
                    raise ValueError("Unsupported image format. Use JPG, PNG or WebP.")
                image = ImageOps.exif_transpose(source)
                image.thumbnail((1024, 1024))
                if image.mode in ("RGBA", "LA", "P"):
                    rgba = image.convert("RGBA")
                    image = Image.alpha_composite(Image.new("RGBA", rgba.size, "white"), rgba).convert("RGB")
                else:
                    image = image.convert("RGB")
                image = ImageOps.autocontrast(image)
                image = ImageEnhance.Contrast(image).enhance(1.5)
                image = ImageEnhance.Sharpness(image).enhance(2.0)
                result = BytesIO()
                image.save(result, "JPEG", quality=90)
                return result.getvalue()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise ValueError("This image could not be read or is too large. Try another JPG, PNG or WebP photo.") from None
