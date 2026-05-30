from .models import SiteSettings


def site_settings(request):
    settings_obj = SiteSettings.objects.order_by('-updated_at').first()
    if settings_obj is None:
        settings_obj = SiteSettings(site_name='airish-fox')
    return {'site_settings': settings_obj}
