from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('contacts', '0002_contactrequest_hardening')]

    operations = [
        migrations.AlterField(
            model_name='contactrequest',
            name='source_page',
            field=models.URLField(blank=True, max_length=500, verbose_name='Страница-источник'),
        ),
    ]
