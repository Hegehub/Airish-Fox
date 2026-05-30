from django.db import migrations, models


def seed_moods(apps, schema_editor):
    MoodCollection = apps.get_model('catalog', 'MoodCollection')
    moods = [
        ('Mint Mood', 'mint-mood', 'Свежие, нежные и мягкие образы в мятном настроении.', '#B8F2D0', 10),
        ('Orange Mood', 'orange-mood', 'Смелые акценты в теплом bitcoin orange вайбе.', '#F7931A', 20),
        ('Cozy Home', 'cozy-home', 'Уютные комплекты для дома, прогулок и slow living.', '#FFF7EA', 30),
        ('Soft Morning', 'soft-morning', 'Легкие образы для спокойного утра и нежных встреч.', '#FFB6C8', 40),
        ('Gift Fox', 'gift-fox', 'Модели, которые легко подарить и красиво упаковать.', '#D95F18', 50),
        ('Fox Pick', 'fox-pick', 'Отборные вещи, которые особенно любит фирменная лисичка.', '#F7931A', 60),
    ]
    for name, slug, description, color_hex, sort_order in moods:
        MoodCollection.objects.get_or_create(slug=slug, defaults={
            'name': name,
            'description': description,
            'color_hex': color_hex,
            'sort_order': sort_order,
            'is_active': True,
        })


class Migration(migrations.Migration):
    dependencies = [('catalog', '0001_initial')]

    operations = [
        migrations.CreateModel(
            name='MoodCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('slug', models.SlugField(max_length=140, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('color_hex', models.CharField(default='#B8F2D0', max_length=7, verbose_name='HEX акцент')),
                ('image', models.ImageField(blank=True, upload_to='moods/', verbose_name='Изображение')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')),
            ],
            options={'verbose_name': 'Mood-подборка', 'verbose_name_plural': 'Mood-подборки', 'ordering': ['sort_order', 'name']},
        ),
        migrations.AddField('product', 'badge', models.CharField(blank=True, default='', max_length=80, verbose_name='Бейдж'), preserve_default=False),
        migrations.AddField('product', 'is_fox_pick', models.BooleanField(default=False, verbose_name='Лисичка советует')),
        migrations.AddField('product', 'is_gift_ready', models.BooleanField(default=False, verbose_name='Готово для подарка')),
        migrations.AddField('product', 'is_daily_pick', models.BooleanField(default=False, verbose_name='Образ дня')),
        migrations.AddField('product', 'whatsapp_message', models.TextField(blank=True, default='', verbose_name='Сообщение WhatsApp'), preserve_default=False),
        migrations.AddField('product', 'telegram_message', models.TextField(blank=True, default='', verbose_name='Сообщение Telegram'), preserve_default=False),
        migrations.AddField('product', 'sort_order', models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')),
        migrations.AddField('product', 'available', models.BooleanField(default=True, verbose_name='Доступен')),
        migrations.AddField('product', 'moods', models.ManyToManyField(blank=True, related_name='products', to='catalog.moodcollection', verbose_name='Mood-подборки')),
        migrations.AlterModelOptions('product', {'verbose_name': 'Товар', 'verbose_name_plural': 'Товары', 'ordering': ['sort_order', '-is_new', '-updated_at', 'name']}),
        migrations.RunPython(seed_moods, migrations.RunPython.noop),
    ]
