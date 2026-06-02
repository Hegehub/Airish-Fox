from django.conf import settings
from django.db import models

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name="wishlists")
    session_key = models.CharField("Session key", max_length=80, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"
        ordering = ["-updated_at"]
    def __str__(self): return f"Wishlist {self.user or self.session_key or self.pk}"
    def get_items_count(self): return self.items.count()

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("catalog.Product", related_name="wishlist_items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Wishlist item"
        verbose_name_plural = "Wishlist items"
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["wishlist", "product"], name="wishlist_unique_product")]
    def __str__(self): return self.product.name
