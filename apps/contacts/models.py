from django.db import models


class ContactRequest(models.Model):
    CONTACT_METHODS = [
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
        ('phone', 'Телефон'),
        ('email', 'Email'),
    ]

    product = models.ForeignKey('catalog.Product', verbose_name='Товар', null=True, blank=True, on_delete=models.SET_NULL, related_name='contact_requests')
    name = models.CharField('Имя', max_length=120)
    phone = models.CharField('Телефон', max_length=40, blank=True)
    email = models.EmailField('Email', blank=True)
    message = models.TextField('Сообщение', blank=True)
    preferred_contact_method = models.CharField('Предпочтительный способ связи', max_length=20, choices=CONTACT_METHODS, default='telegram')
    source_page = models.URLField('Страница-источник', blank=True)
    user_agent = models.TextField('User-Agent', blank=True)
    ip_address = models.GenericIPAddressField('IP-адрес', null=True, blank=True)
    honeypot = models.CharField('Honeypot', max_length=255, blank=True)
    admin_comment = models.TextField('Комментарий администратора', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    is_processed = models.BooleanField('Обработана', default=False)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка от {self.name}'
