# Airish Fox

Production-oriented MVP сайта бренда одежды **airish-fox**: брендовая визитка + мини-витрина коллекции на Django с mood-подборками, фирменной лисичкой, быстрым заказом через мессенджеры и расширяемой архитектурой.

## Возможности

- Django 5.2-ready проект с `config/`, `apps/`, `templates/`, `static/`, `media/`.
- Разделённые настройки: `config.settings.base`, `config.settings.dev`, `config.settings.prod`.
- Приложения:
  - `core` — главная, о бренде, SiteSettings, robots.txt, sitemap.
  - `catalog` — категории, mood-подборки, товары, галерея, detail page, quick order.
  - `reviews` — отзывы клиентов.
  - `contacts` — hardened форма заявки с honeypot, source page, IP/User-Agent и привязкой к товару.
- Django Admin для всех моделей с удобными фильтрами и inline-изображениями.
- Responsive UI на Django Templates + Tailwind CDN + `static/css/site.css`.
- Палитра: Cat Mint `#B8F2D0`, Bitcoin Orange `#F7931A`, Milk Background `#FFF7EA`, Graphite `#242424`, Fox Accent `#D95F18`, Soft Pink `#FFB6C8`.
- SQLite для локальной разработки и PostgreSQL-ready режим через `DATABASE_URL`.
- Dockerfile и docker-compose с web + postgres.
- SEO: canonical, OpenGraph, Twitter Card, sitemap.xml, robots.txt.

## Требования

- Python 3.12+
- pip
- SQLite локально или PostgreSQL для production/dev через Docker
- Docker и Docker Compose опционально

## Переменные окружения

Скопируйте пример:

```bash
cp .env.example .env
```

Ключевые переменные:

```env
DJANGO_SETTINGS_MODULE=config.settings.dev
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
DATABASE_URL=sqlite:///db.sqlite3
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
```

Для production используйте `DJANGO_SETTINGS_MODULE=config.settings.prod`, сильный `SECRET_KEY`, реальные `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` и PostgreSQL URL.

## Локальный запуск без Docker

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте:

- сайт: <http://127.0.0.1:8000/>
- админка: <http://127.0.0.1:8000/admin/>
- sitemap: <http://127.0.0.1:8000/sitemap.xml>
- robots: <http://127.0.0.1:8000/robots.txt>

## Запуск через Docker

```bash
docker compose up --build
```

Миграции:

```bash
docker compose run --rm web python manage.py migrate
```

Создание администратора:

```bash
docker compose run --rm web python manage.py createsuperuser
```

Collectstatic для production-подобной проверки:

```bash
docker compose run --rm web python manage.py collectstatic --noinput
```

Production command в контейнере по умолчанию использует Gunicorn. Для production передайте `DJANGO_SETTINGS_MODULE=config.settings.prod`, `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` и `DATABASE_URL` через окружение:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Как загрузить первые данные через admin

1. Войдите в `/admin/` под superuser.
2. В **Настройки сайта** заполните Brand, Hero, Contacts, Mascot, SEO и Footer.
3. В **Mood-подборки** проверьте автоматически созданные подборки: Mint Mood, Orange Mood, Cozy Home, Soft Morning, Gift Fox, Fox Pick.
4. В **Категории** добавьте категории одежды.
5. В **Товары** добавьте модели:
   - выберите категорию и mood-подборки;
   - заполните описание, цену, размеры, цвет;
   - загрузите главное изображение и галерею;
   - отметьте `Новинка`, `Популярный`, `Лисичка советует`, `Готово для подарка` или `Образ дня` при необходимости;
   - при желании заполните кастомные сообщения WhatsApp/Telegram.
6. В **Отзывы** добавьте активные отзывы.
7. Заявки из формы появятся в **Заявки** с source page, IP/User-Agent и привязкой к товару.

## URL

- `/` — главная.
- `/about/` — о бренде.
- `/collection/` — коллекция.
- `/collection/?category=slug` — фильтр по категории.
- `/collection/?mood=slug` — фильтр по mood-подборке.
- `/collection/?category=slug&mood=slug` — комбинированный фильтр.
- `/collection/new/` — новинки.
- `/collection/product/<slug>/` — страница товара.
- `/reviews/` — отзывы.
- `/contacts/` — контакты и форма заявки.
- `/sitemap.xml` — sitemap.
- `/robots.txt` — robots.txt.

## Быстрый заказ

Кнопка **«Хочу этот образ»** формирует URL для Telegram или WhatsApp на основе `SiteSettings.primary_contact_method` и контактных URL. Текст включает название товара, цвет, размеры и ссылку на страницу товара. Если для товара заполнены `whatsapp_message` или `telegram_message`, используется кастомный текст. Если мессенджеры не настроены, кнопка ведёт на `/contacts/?product=slug`.

## Tailwind / CSS

В MVP сохранён Tailwind CDN, чтобы не усложнять Python-first деплой. Production TODO: добавить Node build-step (`tailwind.config.js`, input.css, purge/content paths, output в `static/css/dist.css`) и убрать CDN. Кастомные production-важные стили уже систематизированы в `static/css/site.css` через CSS variables и компонентные классы.

## Production notes

- Для локальной совместимости `manage.py`, `wsgi.py` и `asgi.py` по умолчанию используют `config.settings.dev`; для production явно задавайте `DJANGO_SETTINGS_MODULE=config.settings.prod`.
- Не храните media uploads на ephemeral FS. Для Docker/VPS подключите volume или объектное хранилище.
- Vercel возможен для serverless Django только с дополнительной конфигурацией и внешним хранением media; для этого проекта предпочтительнее Render, Railway, Fly.io, VPS или Docker-based deployment с PostgreSQL.
- Включите HTTPS-настройки: `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_HSTS_SECONDS=31536000`.
- Настройте `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS` под реальные домены.

## Проверки

```bash
python manage.py check
python manage.py test
python manage.py migrate
```

## Если `git pull` дал конфликты

Пошаговый recovery guide лежит в [`docs/pull-conflicts.md`](docs/pull-conflicts.md). Он описывает безопасные варианты: сохранить локальные изменения через backup/stash, принять входящую версию, оставить локальную версию или вручную убрать conflict markers.

## Ограничения MVP

В MVP намеренно нет корзины, онлайн-оплаты, личного кабинета, регистрации, SPA и блока пакетов услуг. Архитектура подготовлена для дальнейшего расширения: корзина, заказы, платежи, доставка, промокоды, поиск, избранное, REST API и интеграции с Telegram/WhatsApp.
