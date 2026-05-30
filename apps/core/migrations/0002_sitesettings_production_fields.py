from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial')]

    operations = [
        migrations.AddField('sitesettings', 'hero_title', models.CharField(default='Airish Fox', max_length=160, verbose_name='Hero заголовок')),
        migrations.AddField('sitesettings', 'hero_subtitle', models.CharField(blank=True, default='', max_length=240, verbose_name='Hero подзаголовок'), preserve_default=False),
        migrations.AddField('sitesettings', 'hero_cta_primary_label', models.CharField(default='Смотреть коллекцию', max_length=80, verbose_name='Hero CTA primary')),
        migrations.AddField('sitesettings', 'hero_cta_secondary_label', models.CharField(default='Связаться', max_length=80, verbose_name='Hero CTA secondary')),
        migrations.AddField('sitesettings', 'seo_title', models.CharField(blank=True, default='', max_length=180, verbose_name='SEO title'), preserve_default=False),
        migrations.AddField('sitesettings', 'seo_description', models.TextField(blank=True, default='', verbose_name='SEO description'), preserve_default=False),
        migrations.AddField('sitesettings', 'og_image', models.ImageField(blank=True, default='', upload_to='site/og/', verbose_name='OpenGraph изображение'), preserve_default=False),
        migrations.AddField('sitesettings', 'mascot_enabled', models.BooleanField(default=True, verbose_name='Показывать маскота')),
        migrations.AddField('sitesettings', 'mascot_static_image', models.ImageField(blank=True, default='', upload_to='site/mascot/', verbose_name='Статичное изображение маскота'), preserve_default=False),
        migrations.AddField('sitesettings', 'mascot_animation_url', models.URLField(blank=True, default='', verbose_name='URL анимации маскота'), preserve_default=False),
        migrations.AddField('sitesettings', 'mascot_provider', models.CharField(choices=[('static', 'Static image'), ('rive', 'Rive'), ('lottie', 'Lottie')], default='static', max_length=20, verbose_name='Провайдер маскота')),
        migrations.AddField('sitesettings', 'primary_contact_method', models.CharField(choices=[('telegram', 'Telegram'), ('whatsapp', 'WhatsApp'), ('phone', 'Телефон'), ('email', 'Email')], default='telegram', max_length=20, verbose_name='Основной способ связи')),
        migrations.AddField('sitesettings', 'brand_note', models.CharField(blank=True, default='', max_length=240, verbose_name='Брендовая заметка'), preserve_default=False),
        migrations.AddField('sitesettings', 'footer_text', models.TextField(blank=True, default='', verbose_name='Текст в футере'), preserve_default=False),
    ]
