import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0002_moods_and_product_commerce'),
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField('contactrequest', 'message', models.TextField(blank=True, verbose_name='Сообщение')),
        migrations.AddField('contactrequest', 'product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_requests', to='catalog.product', verbose_name='Товар')),
        migrations.AddField('contactrequest', 'source_page', models.URLField(blank=True, default='', verbose_name='Страница-источник'), preserve_default=False),
        migrations.AddField('contactrequest', 'admin_comment', models.TextField(blank=True, default='', verbose_name='Комментарий администратора'), preserve_default=False),
        migrations.AddField('contactrequest', 'user_agent', models.TextField(blank=True, default='', verbose_name='User-Agent'), preserve_default=False),
        migrations.AddField('contactrequest', 'ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP-адрес')),
        migrations.AddField('contactrequest', 'honeypot', models.CharField(blank=True, default='', max_length=255, verbose_name='Honeypot'), preserve_default=False),
    ]
