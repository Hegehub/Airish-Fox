from django.db import models


class SiteSettings(models.Model):
    CONTACT_METHODS = [
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
        ('phone', 'Телефон'),
        ('email', 'Email'),
    ]
    MASCOT_PROVIDERS = [
        ('static', 'Static image'),
        ('rive', 'Rive'),
        ('lottie', 'Lottie'),
    ]

    site_name = models.CharField('Название сайта', max_length=120, default='airish-fox')
    slogan = models.CharField('Слоган', max_length=180, default='Мягкая мята, смелый оранжевый, твой fashion-настрой')
    short_description = models.TextField('Краткое описание', default='Airish Fox — нежная брендовая витрина одежды для уютных, выразительных и ярких образов.')
    hero_title = models.CharField('Hero заголовок', max_length=160, default='Airish Fox')
    hero_subtitle = models.CharField('Hero подзаголовок', max_length=240, blank=True)
    hero_cta_primary_label = models.CharField('Hero CTA primary', max_length=80, default='Смотреть коллекцию')
    hero_cta_secondary_label = models.CharField('Hero CTA secondary', max_length=80, default='Связаться')
    telegram_url = models.URLField('Telegram', blank=True)
    whatsapp_url = models.URLField('WhatsApp', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Телефон', max_length=40, blank=True)
    primary_contact_method = models.CharField('Основной способ связи', max_length=20, choices=CONTACT_METHODS, default='telegram')
    hero_image = models.ImageField('Hero изображение', upload_to='site/', blank=True)
    seo_title = models.CharField('SEO title', max_length=180, blank=True)
    seo_description = models.TextField('SEO description', blank=True)
    og_image = models.ImageField('OpenGraph изображение', upload_to='site/og/', blank=True)
    mascot_enabled = models.BooleanField('Показывать маскота', default=True)
    mascot_static_image = models.ImageField('Статичное изображение маскота', upload_to='site/mascot/', blank=True)
    mascot_animation_url = models.URLField('URL анимации маскота', blank=True)
    mascot_provider = models.CharField('Провайдер маскота', max_length=20, choices=MASCOT_PROVIDERS, default='static')
    brand_note = models.CharField('Брендовая заметка', max_length=240, blank=True)
    footer_text = models.TextField('Текст в футере', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return self.site_name
