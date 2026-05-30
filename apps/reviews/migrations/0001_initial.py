# Generated for Airish Fox MVP
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=120, verbose_name='Имя клиента')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('rating', models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
            ],
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы', 'ordering': ['-created_at']},
        ),
    ]
