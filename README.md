# Airish Fox

Airish Fox — production-ready Django foundation для будущего bright boutique fashion проекта. Этап 1 содержит только базовую структуру, брендовый UI, SVG-лису, healthcheck и подготовку окружений. Каталог, аккаунты, корзина, checkout и платежи на этом этапе не добавляются.

## Stack

- Python 3.12+
- Django 5.2+
- Django Templates
- Tailwind-friendly CSS foundation with Airish Fox design tokens
- PostgreSQL-ready settings через `DATABASE_URL`
- SQLite dev fallback
- Docker и docker-compose
- Redis service подготовлен для будущих Celery tasks
- Gunicorn-ready production requirements
- WhiteNoise для static files

## Структура

```text
airish_fox/
  manage.py
  Dockerfile
  docker-compose.yml
  requirements/
  config/
    settings/
      base.py
      dev.py
      prod.py
  apps/
    core/
  templates/
    pages/
    components/
  static/
    css/
    js/
    images/brand/
  media/
  docs/
```

## Локальный запуск без Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Приложение будет доступно на <http://127.0.0.1:8000/>.

## Запуск через Docker

```bash
cp .env.example .env
docker-compose up --build
```

Для подключения Django к PostgreSQL в Docker замените `DATABASE_URL` в `.env`:

```env
DATABASE_URL=postgres://airish_fox:airish_fox@postgres:5432/airish_fox
```

## Полезные команды

```bash
python manage.py check
python manage.py test
python manage.py migrate
python manage.py createsuperuser
```

## Admin и service URLs

- `/` — главная страница.
- `/health/` — healthcheck.
- `/robots.txt` — robots.txt.
- `/admin/` — Django admin.

## Brand assets

SVG-файлы бренда находятся в `static/images/brand/`:

- `fox-logo.svg`
- `fox-mark.svg`
- `fox-mascot-idle.svg`
- `fox-favicon.svg`

Правило бренда: emoji не использовать как production logo, favicon или mascot. Для Airish Fox используется только оригинальная SVG-лиса.

Подробнее: `docs/brand.md`.

## Следующие этапы

В следующих этапах будут добавлены:

- каталог;
- аккаунты;
- корзина;
- checkout;
- 2C2P by Antom;
- Google Maps;
- mascot animation.

## Catalog app

Этап 2 добавляет `apps/catalog`: каталог одежды с категориями, fashion-коллекциями, mood-подборками, товарами, вариантами товара, изображениями, SEO-полями, фильтрами и Django Admin.

### Product vs ProductVariant

`Product` — родительская карточка товара: название, категория, коллекции, mood-подборки, описание, материалы, SEO и брендовые признаки.

`ProductVariant` — продаваемая единица товара: SKU, размер, цвет, цена и остаток.

> Важно: цена, размер, цвет и остаток хранятся только на уровне `ProductVariant`. Не добавляйте цену напрямую в `Product`.

### Как добавить каталог в admin

1. Создайте категорию в **Каталог → Категории**:
   - заполните `name`, `slug`, описание и при необходимости изображение;
   - оставьте `is_active=True`, чтобы категория участвовала в фильтрах.
2. Создайте mood collection в **Каталог → Mood-подборки**:
   - укажите `name`, `slug`, описание и `color_hex`;
   - примеры: `Mint Mood`, `Orange Mood`, `Cozy Home`, `Gift Fox`, `Fox Pick`.
3. Создайте fashion-коллекцию в **Каталог → Коллекции**:
   - например `Summer Drop`, `Home Capsule`, `New Season`.
4. Создайте товар в **Каталог → Товары**:
   - выберите категорию;
   - добавьте коллекции и mood-подборки;
   - заполните `short_description`, описание, материал и уход;
   - при необходимости заполните `badge`.
5. Добавьте варианты товара inline в карточке товара:
   - `sku`, `size`, `color_name`, `color_hex`, `price`, `compare_at_price`, `stock_quantity`;
   - вариант должен быть `is_active=True`, чтобы товар отображался в каталоге.
6. Добавьте фото товара inline:
   - изображения загружаются в `media/catalog/products/`;
   - разрешены `jpg`, `jpeg`, `png`, `webp`, максимум 5 MB;
   - SVG для catalog images запрещён, SVG используется только для brand assets.

### Брендовые признаки товара

В карточке товара можно отметить:

- `is_new` — товар попадёт на `/new/` и в блок новинок на главной;
- `is_featured` — товар попадёт в featured-блок на главной;
- `is_fox_pick` — товар попадёт в Fox picks;
- `is_gift_ready` — товар получит gift-ready бейдж;
- `badge` — ручной бейдж, например `Новинка`, `Лисичка советует`, `Gift Ready`, `Limited`, `Bestseller`.

### Страницы каталога

- `/catalog/` — каталог с фильтрами `category`, `mood`, `collection`, `new=1`, `fox_pick=1`.
- `/catalog/<slug>/` — detail page товара.
- `/new/` — новинки.
- `/collections/` — список fashion-коллекций.
- `/collections/<slug>/` — товары коллекции.
- `/moods/<slug>/` — товары mood-подборки.

На этапе 2 нет корзины, checkout, оплаты, аккаунтов, wishlist, reviews, loyalty и Google Maps. CTA на detail page — только disabled placeholder `Корзина скоро`.

## Accounts

Этап 3 добавляет `apps/accounts`: регистрацию, вход, выход, личный кабинет покупателя, профиль и адреса доставки на стандартной Django auth-системе без custom User model.

### Что доступно покупателю

- Регистрация с `username`, обязательным уникальным `email` и паролем.
- Вход и выход через стандартные Django auth views.
- Личный кабинет с email, телефоном, сохранёнными размерами, любимым mood и default shipping address.
- Редактирование `CustomerProfile` для будущего size memory и персональных рекомендаций.
- Управление несколькими адресами доставки.
- Только один адрес пользователя может быть `default shipping`.
- Смена пароля через встроенный Django password change flow.

### CustomerProfile

`CustomerProfile` создаётся автоматически при создании `User` через signal. Профиль хранит:

- phone;
- birthday;
- preferred size top / bottom;
- preferred fit: `slim`, `regular`, `relaxed`, `oversized`;
- favorite color;
- favorite mood;
- marketing consent.

Эти поля подготовлены для будущих этапов: checkout address reuse, orders в кабинете, персональные рекомендации и size memory.

### Addresses

`Address` хранит данные доставки покупателя: получатель, телефон, страна, город, район, ward, street address, postal code и delivery notes.

Безопасность:

- страницы кабинета доступны только авторизованным пользователям;
- пользователь видит только свои адреса;
- редактировать или удалить чужой адрес нельзя;
- формы защищены CSRF;
- пароли не логируются и не выводятся.

### Account URLs

- `/account/register/` — регистрация.
- `/account/login/` — вход.
- `/account/logout/` — выход.
- `/account/` — dashboard.
- `/account/profile/` — редактирование профиля.
- `/account/password/` — смена пароля.
- `/account/addresses/` — список адресов.
- `/account/addresses/new/` — новый адрес.

### Как проверить вручную

```bash
python manage.py migrate
python manage.py runserver
```

1. Откройте `/account/register/` и создайте покупателя.
2. После регистрации проверьте redirect в `/account/`.
3. Перейдите в `/account/profile/` и заполните размеры, посадку и любимый mood.
4. Перейдите в `/account/addresses/new/` и добавьте default shipping address.
5. Добавьте второй default shipping address и убедитесь, что первый перестал быть default.
6. Выйдите через navbar и проверьте, что `/account/` снова требует вход.

## Этап 4 — Корзина

Этап 4 добавляет `apps/cart`: production-ready корзину для гостей и авторизованных покупателей. Корзина работает только с продаваемыми единицами `ProductVariant`, а не с родительским `Product`.

### Как работает guest cart

- Для гостя корзина хранится в базе как `Cart` с `session_key` и статусом `active`.
- Корзина не создаётся просто от просмотра страниц: navbar использует лёгкий context processor и не создаёт пустую cart без необходимости.
- При первом добавлении товара создаётся session cart, а её id сохраняется в session для безопасного merge после login.

### Как работает user cart

- Для авторизованного пользователя используется активная `Cart` с FK на `User`.
- `CartItem` хранит `variant`, `quantity` и `unit_price_snapshot`.
- Цена берётся только с сервера из `ProductVariant.price`; цена из request не принимается.
- `subtotal` и `line total` считаются на сервере.

### Merge после login

После успешного входа гостевая корзина объединяется с активной корзиной пользователя через signal `user_logged_in`:

- если у пользователя нет active cart — она создаётся;
- если variant уже есть в user cart — quantity аккуратно суммируется;
- итоговое quantity не превышает `stock_quantity`;
- guest cart получает статус `converted`;
- дубли `CartItem` не создаются.

### Stock rules

Stock не уменьшается при добавлении в корзину. Остатки будут списываться только после успешной оплаты на будущем этапе.

Корзина проверяет:

- product active;
- variant active;
- stock_quantity > 0;
- requested quantity <= stock_quantity.

Если товар или вариант стали недоступны, cart page показывает предупреждение. Checkout и оплата на этом этапе не реализуются.

### Cart URLs

- `/cart/` — страница корзины.
- `/cart/add/` — POST add-to-cart.
- `/cart/update/<item_id>/` — POST обновления количества.
- `/cart/remove/<item_id>/` — POST удаления позиции.
- `/cart/clear/` — POST очистки корзины.

### Cart models

- `Cart` — владелец корзины: `user` или `session_key`, `status`, timestamps.
- `CartItem` — позиция корзины: `cart`, `variant`, `quantity`, `unit_price_snapshot`, timestamps.

### Команды проверки

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py check
```

Следующий этап — оформление заказа. На этапе 4 нет checkout, orders, payment, PromoCode, 2C2P by Antom и платёжных транзакций.

## Orders and Checkout

Этап 5 добавляет архитектуру оформления заказа без реальной онлайн-оплаты: `apps/shipping`, `apps/promotions`, `apps/orders` и `apps/checkout`.

### ShippingMethod

Способы доставки добавляются через Django Admin в разделе **Доставка → Способы доставки**.

Рекомендуемые MVP-варианты:

- `Standard delivery` — обычная доставка;
- `Express delivery` — ускоренная доставка;
- `Store pickup` с кодом `store-pickup` — самовывоз, для которого адрес доставки не обязателен.

Каждый способ доставки имеет `base_price`, `is_active` и `sort_order`. В checkout доступны только active методы.

### PromoCode

Промокоды добавляются через Django Admin в разделе **Промокоды**.

Поддерживаются типы:

- `percent` — процентная скидка от subtotal;
- `fixed` — фиксированная скидка.

Правила промокодов:

- inactive промокод не применяется;
- expired промокод не применяется;
- `max_uses` ограничивает количество использований;
- `minimum_order_amount` проверяется перед применением;
- скидка не может быть больше subtotal;
- процентная скидка ограничена диапазоном 0–100%.

### Как работает checkout

1. Покупатель открывает `/checkout/`.
2. Если active cart пуста, пользователь возвращается в `/cart/` с сообщением.
3. Checkout form собирает имя, email, телефон, адрес, способ доставки, промокод, комментарий и gift options.
4. `CheckoutService` в `apps/checkout/services.py` внутри `transaction.atomic()` заново проверяет корзину, товары, варианты и остатки.
5. Создаётся `Order` со статусом `pending_payment` и `payment_status=unpaid`.
6. Создаются `OrderItem` snapshot-записи: название товара, SKU, размер, цвет, количество и цена фиксируются на момент заказа.
7. `Cart.status` становится `converted`, но `CartItem` физически не удаляются.
8. Пользователь переходит на `/orders/<number>/`, где видит безопасный шаг перехода к оплате через hosted checkout провайдера.

Stock не уменьшается при создании pending order. Остатки списываются только после подтверждённой оплаты через signed webhook на этапе 6.

### Order access

- Авторизованный пользователь видит только свои заказы.
- Гость может открыть созданный заказ в текущей session, если номер заказа сохранён в session.
- Чужие заказы защищены и возвращают 404.

### Checkout URLs

- `/checkout/` — форма оформления заказа.
- `/orders/<number>/` — детали заказа и pending payment page.
- `/account/orders/` — история заказов авторизованного пользователя.

На этапе 5 ещё не было payment gateway, карточных форм, хранения карточных данных и интеграции 2C2P by Antom. Этап 6 добавляет только hosted / redirect payment layer без обработки карточных данных на сайте.

## Payments: 2C2P by Antom

Этап 6 добавляет payment layer для hosted / redirect online payments через 2C2P by Antom. Сайт Airish Fox не хранит card data и не показывает собственные поля card number / CVV / expiry date: покупатель уходит на защищённую страницу платёжного провайдера.

### Sandbox-first configuration

Все credentials задаются только через environment variables:

- `ANTOM_ENV=sandbox`
- `ANTOM_GATEWAY_URL` — sandbox или live endpoint Antom hosted payment API.
- `ANTOM_CLIENT_ID` — client id / merchant id из Antom dashboard.
- `ANTOM_MERCHANT_PRIVATE_KEY` — merchant private key в PEM-формате, хранить только в env/secret manager.
- `ANTOM_PUBLIC_KEY` — Antom public key для проверки webhook signatures.
- `ANTOM_KEY_VERSION` — версия ключа из Antom dashboard.
- `ANTOM_PAYMENT_CURRENCY=VND`
- `ANTOM_NOTIFY_URL` — публичный webhook URL, например `https://example.com/payments/antom/notify/`.
- `ANTOM_RETURN_URL` — return URL, например `https://example.com/payments/antom/return/`.
- `ANTOM_TIMEOUT_SECONDS=20`
- `ANTOM_PAYMENTS_ENABLED=True` — в production заставляет settings проверить обязательные credentials.

Private key never committed. Если ключ утёк — rotate keys immediately.

### Payment flow

1. Checkout создаёт `Order` со статусом `pending_payment`.
2. На странице заказа пользователь нажимает “Оплатить картой / онлайн”.
3. `apps/payments` создаёт или переиспользует `PaymentTransaction` по idempotent `payment_request_id`.
4. `Antom2C2PPaymentProvider` формирует hosted payment payload и отправляет signed request в Antom.
5. Пользователь перенаправляется на provider checkout URL.
6. Browser return URL показывает только pending/success/failed UI и сам по себе не подтверждает оплату.
7. Финальное подтверждение оплаты происходит через signed webhook `/payments/antom/notify/`.
8. После valid paid webhook order получает `payment_status=paid`, `status=processing`, а stock уменьшается ровно один раз.

### Payment URLs

- `/payments/antom/create/<order_number>/` — POST, создать hosted payment и redirect к provider.
- `/payments/antom/return/` — GET, browser return status page.
- `/payments/antom/notify/` — POST, signed webhook/notification endpoint.

### Security notes

- No PAN, CVV or expiry date is stored or processed by Airish Fox.
- Use HTTPS in production for both notify and return URLs.
- `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` and secure cookies must be configured.
- Webhook endpoint must be publicly reachable by Antom.
- Sandbox and live credentials must not be mixed.
- Do not log private keys or sensitive authorization headers.
- Restrict production logs and rotate keys if leaked.

### Before live launch verify with current Antom docs

- VND amount format / minor unit rules.
- Signature canonical string format.
- Webhook signature headers and key version format.
- Notification response format expected by Antom.
- Payment status mapping from live response examples.
- Live dashboard notify URL and return URL.
- Live credentials and key rotation policy.

### Testing payments

Unit tests mock Antom HTTP calls and signature verification; they do not perform real provider requests.

```bash
python manage.py test apps.payments
python manage.py test
```

## Store Location / Google Maps

Этап 7 добавляет `apps/store_locator`: физические магазины Airish Fox во Вьетнаме, Google Maps layer, fallback без API key, часы работы, контакты, маршрут и самовывоз.

### Как создать магазин через Django Admin

1. Откройте **Магазины → Магазины**.
2. Создайте `StoreLocation`:
   - заполните `name`, `slug`, короткое описание и адрес;
   - укажите `city`, `district`, `street_address` или `full_address`;
   - добавьте координаты `latitude` и `longitude` из Google Maps;
   - отметьте `is_active=True`;
   - для основного магазина включите `is_main_store=True`;
   - включите `pickup_available` и `fitting_available`, если доступны самовывоз и примерка.
3. Добавьте контакты: телефон, email, WhatsApp, Telegram, Instagram.
4. При необходимости заполните `google_maps_place_url` и `google_maps_embed_url`.
5. Добавьте главное изображение и gallery-фото через inline `StorePhoto`.
6. Заполните часы работы через inline `StoreOpeningHour` для дней 0–6, где 0 — Monday, 6 — Sunday.

### Google Maps configuration

Нужные переменные окружения:

```env
GOOGLE_MAPS_API_KEY=
GOOGLE_MAPS_MAP_ID=
GOOGLE_MAPS_DEFAULT_ZOOM=15
```

API key создаётся в Google Cloud Console. Для production ключ нужно ограничить:

- по HTTP referrers / доменам production-сайта;
- только нужными Google Maps APIs;
- не использовать один ключ для sandbox и production без необходимости;
- не коммитить ключ в репозиторий.

Если `GOOGLE_MAPS_API_KEY` не задан, страницы `/store/` и `/store/<slug>/` не подключают Google Maps JS и показывают fallback-карточку с адресом, координатами, кнопкой “Построить маршрут” и ссылкой “Открыть в Google Maps”, если она заполнена.

### Store URLs

- `/store/` — список активных магазинов и карта главного магазина.
- `/store/<slug>/` — детальная страница магазина с адресом, часами работы, контактами, картой и gallery.

### Самовывоз в checkout

Если checkout уже включён и в `ShippingMethod` есть активный метод с кодом `store-pickup`, форма checkout показывает поле выбора магазина самовывоза при наличии активных `StoreLocation` с `pickup_available=True`. Для самовывоза `shipping_total` считается `0`, а заказ сохраняет:

- `pickup_store` — ссылку на магазин;
- `pickup_store_name` — snapshot названия;
- `pickup_store_address` — snapshot адреса.

Checkout, payments и stock logic не переписываются: оплата 2C2P by Antom остаётся в payment layer, а списание stock происходит только после подтверждённой оплаты.

## Brand Experience Layer

Этап 8 добавляет дополнительный брендовый слой Airish Fox поверх уже существующего commerce foundation. Эти функции опциональны и не являются зависимостью checkout, cart или payment flow: если quiz, wishlist, drops или story blocks отключены/пустые, каталог, корзина, оформление и оплата продолжают работать.

### SVG Fox Mascot System

Расширенные mascot assets лежат в `static/images/brand/mascot/`:

- `fox-idle.svg`
- `fox-happy.svg`
- `fox-thinking.svg`
- `fox-cart-empty.svg`
- `fox-payment-success.svg`
- `fox-gift.svg`
- `fox-map-guide.svg`
- `fox-pick.svg`

Компонент `templates/components/mascot.html` поддерживает states: `idle`, `happy`, `thinking`, `cart_empty`, `payment_success`, `gift`, `map_guide`, `fox_pick`. Если state неизвестен, используется idle SVG; если SVG не загрузится, fallback — базовый `fox-mascot-idle.svg`. Emoji не используются как production logo или mascot.

Чтобы заменить mascot assets, положите безопасный SVG без external links и scripts в `static/images/brand/mascot/` с тем же именем файла. Цвета должны оставаться в палитре Airish Fox: mint, orange, milk, graphite, fox и soft pink.

### Mood Shopping

Mood-подборки управляются через `catalog.MoodCollection`. Главная страница показывает блок “Выберите настроение”, а карточки mood ведут в каталог с фильтром `/catalog/?mood=<slug>`. Пустые подборки показывают мягкий empty state с SVG-лисой.

### Fox Style Quiz

`apps/style_quiz` — простой quiz без AI и внешних API:

- вопросы `StyleQuizQuestion` управляются через admin;
- варианты `StyleQuizOption` могут ссылаться на mood, category, preferred color и gift intent;
- отправка сохраняет `StyleQuizSubmission` с `answers` и `result_url`;
- пользователь перенаправляется в каталог с query params для подборки.

URL:

- `/style-quiz/`
- `/style-quiz/results/`

### Gift Mode

Gift Mode использует существующие поля заказа: `is_gift`, `gift_wrap`, `gift_message`, `hide_price_in_package`. Checkout показывает отдельный “Подарочный режим” с mascot state `gift`. Сообщение ограничено 500 символами. Если `is_gift=False`, checkout service очищает gift message как раньше.

### Wishlist

`apps/wishlist` добавляет избранное без влияния на checkout:

- гости используют session wishlist;
- авторизованные пользователи используют user wishlist;
- при login гостевой wishlist объединяется с пользовательским;
- product card и product detail имеют POST-кнопку “В избранное”;
- empty wishlist показывает SVG-лису.

URL:

- `/wishlist/`
- `POST /wishlist/add/<product_id>/`
- `POST /wishlist/remove/<product_id>/`
- `POST /wishlist/toggle/<product_id>/`

### Limited Drops

`apps/drops` добавляет лимитированные drops:

- `ProductDrop` управляет hero, продуктами, временем старта/окончания, countdown и waitlist;
- `DropWaitlistEntry` сохраняет email и не допускает дубликаты email внутри одного drop;
- products показываются только если они active.

URL:

- `/drops/`
- `/drops/<slug>/`
- `POST /drops/<slug>/waitlist/`

### Admin feature management

Через admin доступны:

- `BrandFeatureToggle` — optional feature flags (`mascot_enabled`, `style_quiz_enabled`, `gift_mode_enabled`, `limited_drops_enabled`, `wishlist_enabled`, `mood_shopping_enabled`);
- `HomepageStoryBlock` — story blocks на главной;
- `BrandBadge` — брендовые badge metadata;
- `StyleQuizQuestion`, `StyleQuizOption`, readonly `StyleQuizSubmission`;
- `Wishlist` / `WishlistItem`;
- `ProductDrop` / `DropWaitlistEntry`.

### Production safety

- Никакие wow-функции не меняют payment provider и не трогают 2C2P by Antom.
- Wishlist, drops и quiz используют обычные Django views/forms и CSRF для POST.
- JS в `static/js/brand.js` — progressive enhancement only.
- CSS-анимации учитывают `prefers-reduced-motion`.
- SVG-лиса используется как брендовый mascot; emoji не используются как логотип или production mascot.

## Production hardening

Stage 9 tightens Airish Fox for launch readiness without adding new commerce flows. Production uses `config.settings.prod`, requires environment-provided `SECRET_KEY` and `ALLOWED_HOSTS`, supports `CSRF_TRUSTED_ORIGINS`, and makes the admin path configurable with `ADMIN_URL`.

### Security checklist

- Use `DEBUG=False` and `DJANGO_SETTINGS_MODULE=config.settings.prod` in production.
- Set `ADMIN_URL=secure-admin/` or another non-default private path.
- Keep `SECURE_SSL_REDIRECT`, secure cookies and HSTS enabled behind HTTPS.
- Store Antom private/public keys only in environment variables.
- Do not collect or store card number, CVV or expiry date on Airish Fox pages.
- Use rate limits (`RATE_LIMIT_LOGIN`, `RATE_LIMIT_REGISTER`, `RATE_LIMIT_CHECKOUT`, `RATE_LIMIT_PAYMENT_CREATE`) and the checkout honeypot to reduce abuse.

### SEO and performance

- `sitemap.xml` includes public home, catalog, product, category, collection, mood, store, drops and style quiz pages.
- `robots.txt` disallows admin/account/cart/checkout/payment paths and points crawlers to the sitemap.
- SEO meta includes canonical, OpenGraph and Twitter card tags.
- Product detail pages include Product JSON-LD with VND offers and stock availability.
- Catalog/payment models include additional indexes for common production queries.

### Observability and Celery

Set `SENTRY_DSN` to enable optional Sentry monitoring. Logging is configured for `django.request`, `apps.payments`, `apps.orders`, `apps.checkout` and `apps.cart` without logging private keys or payment-sensitive data.

Start a Celery worker when background tasks are enabled:

```bash
celery -A config worker -l info
```

### Payment reconciliation

Pending Antom transactions can be audited with:

```bash
python manage.py reconcile_payments --dry-run
```

The command intentionally does not guess live provider APIs; see `docs/payments-antom.md` for the go-live checklist.

### Production documentation

- `docs/deployment.md` — deployment, static files, Docker and Celery.
- `docs/security.md` — secrets, HTTPS, admin URL, form protection and payment logging rules.
- `docs/payments-antom.md` — hosted Antom flow, webhook safety and reconciliation.
- `docs/google-maps.md` — Google Maps key restrictions and fallback behavior.
- `docs/admin-guide.md` — operational admin workflows.

## Final launch QA checklist

Before live launch, verify:

- `python manage.py check`, `python manage.py test`, `python manage.py migrate`, `python manage.py collectstatic --noinput` and `python manage.py check --deploy` pass in an environment with dependencies installed.
- `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `ADMIN_URL`, email SMTP settings, Antom keys and Google Maps keys are configured from environment variables.
- The Antom payment flow remains hosted/redirect only; Airish Fox must not collect or store card number, CVV or expiry date.
- Antom dashboard notification URL points to `/payments/antom/notify/` on a public HTTPS domain, and the return URL points to `/payments/antom/return/`.
- Google Maps API key is restricted by HTTP referrer/domain and limited to the APIs actually used by the store locator.
- Production media uses durable S3-compatible/object storage or an equivalent media strategy; local media is for development only.
- Preferred production hosting is server/Docker oriented: VPS, Render, Railway, Fly.io or another platform that supports web workers, Redis/Celery, media storage and public payment webhooks. Vercel is not ideal for this full Django e-commerce deployment.

See `docs/deployment.md`, `docs/security.md`, `docs/payment-antom.md`, `docs/google-maps.md`, `docs/admin-guide.md` and `docs/brand.md` for operational details.

### Docker prod-like start

For a production-like container run, provide `.env` with production values and use:

```bash
docker compose -f docker-compose.prod.yml up --build
```

Then run migrations, collect static files and create an admin user from the web container as needed.

## Vercel deployment notes

Vercel's Python builder parses dependency files before running Django, so the root `requirements.txt` and `requirements/prod.txt` are intentionally flat and do not use recursive `-r` includes.

Set these Vercel Environment Variables before deploying:

```env
DJANGO_SETTINGS_MODULE=config.settings.prod
SECRET_KEY=<real-secret>
DEBUG=False
ALLOWED_HOSTS=airish-fox.vercel.app,.vercel.app
CSRF_TRUSTED_ORIGINS=https://airish-fox.vercel.app
ADMIN_URL=secure-admin/
DATABASE_URL=<external-postgresql-url>
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=0
ANTOM_PAYMENTS_ENABLED=False
```

Do not commit secrets to the repository. Use an external PostgreSQL database; Vercel serverless functions are not a replacement for persistent database/media storage, Redis workers or long-running Celery processes.
