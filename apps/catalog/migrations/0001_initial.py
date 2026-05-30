# Generated for Airish Fox MVP
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('slug', models.SlugField(max_length=140, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='categories/', verbose_name='Изображение')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')),
            ],
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории', 'ordering': ['sort_order', 'name']},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160, verbose_name='Название')),
                ('slug', models.SlugField(max_length=180, unique=True, verbose_name='Slug')),
                ('short_description', models.CharField(max_length=240, verbose_name='Краткое описание')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('sizes', models.CharField(help_text='Например: XS, S, M, L', max_length=120, verbose_name='Размеры')),
                ('color_name', models.CharField(max_length=80, verbose_name='Название цвета')),
                ('color_hex', models.CharField(default='#B8F2D0', max_length=7, verbose_name='HEX цвета')),
                ('main_image', models.ImageField(blank=True, upload_to='products/', verbose_name='Главное изображение')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Популярный')),
                ('is_new', models.BooleanField(default=False, verbose_name='Новинка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='catalog.category', verbose_name='Категория')),
            ],
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары', 'ordering': ['-is_new', '-created_at', 'name']},
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/gallery/', verbose_name='Изображение')),
                ('alt_text', models.CharField(blank=True, max_length=180, verbose_name='Alt-текст')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.product', verbose_name='Товар')),
            ],
            options={'verbose_name': 'Изображение товара', 'verbose_name_plural': 'Изображения товаров', 'ordering': ['sort_order', 'id']},
        ),
    ]
