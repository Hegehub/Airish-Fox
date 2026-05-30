from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField('Название сайта', max_length=120, default='airish-fox')
    slogan = models.CharField('Слоган', max_length=180, default='Мягкая мята, смелый оранжевый, твой fashion-настрой')
    short_description = models.TextField('Краткое описание', default='Airish Fox — нежная брендовая витрина одежды для уютных, выразительных и ярких образов.')
    telegram_url = models.URLField('Telegram', blank=True)
    whatsapp_url = models.URLField('WhatsApp', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Телефон', max_length=40, blank=True)
    hero_image = models.ImageField('Hero изображение', upload_to='site/', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return self.site_name
