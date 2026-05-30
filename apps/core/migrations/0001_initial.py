# Generated for Airish Fox MVP
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='airish-fox', max_length=120, verbose_name='Название сайта')),
                ('slogan', models.CharField(default='Мягкая мята, смелый оранжевый, твой fashion-настрой', max_length=180, verbose_name='Слоган')),
                ('short_description', models.TextField(default='Airish Fox — нежная брендовая витрина одежды для уютных, выразительных и ярких образов.', verbose_name='Краткое описание')),
                ('telegram_url', models.URLField(blank=True, verbose_name='Telegram')),
                ('whatsapp_url', models.URLField(blank=True, verbose_name='WhatsApp')),
                ('instagram_url', models.URLField(blank=True, verbose_name='Instagram')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=40, verbose_name='Телефон')),
                ('hero_image', models.ImageField(blank=True, upload_to='site/', verbose_name='Hero изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={'verbose_name': 'Настройки сайта', 'verbose_name_plural': 'Настройки сайта'},
        ),
    ]
