# Generated for Airish Fox MVP
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Имя')),
                ('phone', models.CharField(blank=True, max_length=40, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('preferred_contact_method', models.CharField(choices=[('telegram', 'Telegram'), ('whatsapp', 'WhatsApp'), ('phone', 'Телефон'), ('email', 'Email')], default='telegram', max_length=20, verbose_name='Предпочтительный способ связи')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('is_processed', models.BooleanField(default=False, verbose_name='Обработана')),
            ],
            options={'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки', 'ordering': ['-created_at']},
        ),
    ]
