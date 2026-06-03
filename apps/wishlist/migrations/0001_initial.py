# Generated manually for Airish Fox wishlist stage 8.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("catalog", "0001_initial")]
    operations = [
        migrations.CreateModel(name="Wishlist", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("session_key", models.CharField(blank=True, db_index=True, max_length=80, verbose_name="Session key")), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="wishlists", to=settings.AUTH_USER_MODEL))], options={"verbose_name":"Wishlist","verbose_name_plural":"Wishlists","ordering":["-updated_at"]}),
        migrations.CreateModel(name="WishlistItem", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("created_at", models.DateTimeField(auto_now_add=True)), ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="wishlist_items", to="catalog.product")), ("wishlist", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="wishlist.wishlist"))], options={"verbose_name":"Wishlist item","verbose_name_plural":"Wishlist items","ordering":["-created_at"], "constraints":[models.UniqueConstraint(fields=("wishlist", "product"), name="wishlist_unique_product")]}),
    ]
