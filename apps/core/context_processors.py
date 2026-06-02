"""Template context processors for brand defaults."""


def brand(request):
    """Expose Airish Fox brand defaults to every template."""
    return {
        "brand_name": "Airish Fox",
        "brand_tagline": "Мягкая мода с лисьим характером",
        "brand_description": (
            "Airish Fox — будущий boutique fashion brand с ярким, нежным "
            "и premium-настроением."
        ),
    }
