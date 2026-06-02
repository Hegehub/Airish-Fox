"""Catalog service helpers and validators."""

from pathlib import Path

from django.core.exceptions import ValidationError

MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_image_size(image):
    """Reject catalog images larger than the production-safe upload limit."""
    if image and image.size > MAX_IMAGE_SIZE_BYTES:
        raise ValidationError("Размер изображения не должен превышать 5 MB.")


def validate_image_extension(image):
    """Allow only raster formats for catalog images; SVG is reserved for brand assets."""
    extension = Path(image.name).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        allowed = ", ".join(sorted(ext.lstrip(".") for ext in ALLOWED_IMAGE_EXTENSIONS))
        raise ValidationError(f"Неподдерживаемый формат изображения. Разрешены: {allowed}.")
