# Admin guide

The admin URL is configurable with `ADMIN_URL` and should not remain `/admin/` in production.

Recommended admin workflows:

- Catalog: manage categories, products, variants, images and stock.
- Orders: inspect order snapshots, payment status and manual review flags.
- Payments: inspect transactions and webhook events. Raw request/response fields are read-only audit data.
- Promotions and shipping: maintain active promo codes and delivery methods.
- Store locator: manage physical store address, coordinates, opening hours and photos.
- Brand layer: manage feature toggles, homepage story blocks, badges, drops and quiz questions.

Never paste private payment keys or card data into admin fields.
