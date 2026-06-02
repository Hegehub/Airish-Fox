"""Catalog class-based views."""

import json

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Category, Collection, MoodCollection, Product


def active_product_queryset():
    """Return active products with at least one active variant and optimized relations."""
    return (
        Product.objects.filter(is_active=True, variants__is_active=True)
        .select_related("category")
        .prefetch_related("moods", "collections", "variants", "images")
        .distinct()
    )


class CatalogContextMixin:
    page_title = "Каталог Airish Fox"
    meta_description = "Каталог одежды Airish Fox: категории, коллекции, mood-подборки и fox picks."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("categories", Category.objects.filter(is_active=True))
        context.setdefault("moods", MoodCollection.objects.filter(is_active=True))
        context.setdefault("collections", Collection.objects.filter(is_active=True))
        context.setdefault("page_title", self.page_title)
        context.setdefault("meta_description", self.meta_description)
        context.setdefault("canonical_url", self.request.build_absolute_uri(self.request.path))
        context.setdefault("og_title", context["page_title"])
        context.setdefault("og_description", context["meta_description"])
        return context


class ProductListView(CatalogContextMixin, ListView):
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = active_product_queryset()
        self.current_category = None
        self.current_mood = None
        self.current_collection = None

        category_slug = self.request.GET.get("category")
        mood_slug = self.request.GET.get("mood")
        collection_slug = self.request.GET.get("collection")
        color_value = self.request.GET.get("color")

        if category_slug:
            self.current_category = get_object_or_404(Category, slug=category_slug, is_active=True)
            queryset = queryset.filter(category=self.current_category)
        if mood_slug:
            self.current_mood = get_object_or_404(MoodCollection, slug=mood_slug, is_active=True)
            queryset = queryset.filter(moods=self.current_mood)
        if collection_slug:
            self.current_collection = get_object_or_404(Collection, slug=collection_slug, is_active=True)
            queryset = queryset.filter(collections=self.current_collection)
        if self.request.GET.get("new") == "1":
            queryset = queryset.filter(is_new=True)
        if self.request.GET.get("fox_pick") == "1":
            queryset = queryset.filter(is_fox_pick=True)
        if self.request.GET.get("gift_ready") == "1":
            queryset = queryset.filter(is_gift_ready=True)
        if color_value:
            queryset = queryset.filter(variants__color_hex__icontains=color_value.strip().lstrip("#"))
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_category = getattr(self, "current_category", None)
        current_mood = getattr(self, "current_mood", None)
        current_collection = getattr(self, "current_collection", None)
        context["current_category"] = current_category
        context["current_mood"] = current_mood
        context["current_collection"] = current_collection
        if current_category:
            context["page_title"] = current_category.seo_title or current_category.name
            context["meta_description"] = current_category.seo_description or current_category.description
        elif current_mood:
            context["page_title"] = current_mood.seo_title or current_mood.name
            context["meta_description"] = current_mood.seo_description or current_mood.description
        elif current_collection:
            context["page_title"] = current_collection.seo_title or current_collection.name
            context["meta_description"] = current_collection.seo_description or current_collection.description
        context["og_title"] = context["page_title"]
        context["og_description"] = context["meta_description"]
        return context


class ProductDetailView(DetailView):
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return active_product_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        mood_ids = list(product.moods.values_list("id", flat=True))
        related = active_product_queryset().filter(Q(category=product.category) | Q(moods__id__in=mood_ids)).exclude(pk=product.pk)[:4]
        main_image = product.get_main_image()
        default_variant = product.get_active_variants().filter(stock_quantity__gt=0).first()
        min_price = product.get_min_price()
        active_variant = default_variant or product.get_active_variants().first()
        product_schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": product.name,
            "description": product.seo_description or product.short_description,
            "brand": {"@type": "Brand", "name": "Airish Fox"},
            "category": product.category.name,
            "url": self.request.build_absolute_uri(product.get_absolute_url()),
            "offers": {
                "@type": "Offer",
                "priceCurrency": "VND",
                "price": str(min_price or 0),
                "availability": "https://schema.org/InStock" if product.is_available() else "https://schema.org/OutOfStock",
            },
        }
        if main_image:
            product_schema["image"] = self.request.build_absolute_uri(main_image.image.url)
        if active_variant:
            product_schema["sku"] = active_variant.sku
        context.update(
            {
                "variants": product.get_active_variants(),
                "default_variant": default_variant,
                "gallery": product.images.all(),
                "related_products": related,
                "page_title": product.seo_title or product.name,
                "meta_description": product.seo_description or product.short_description,
                "canonical_url": self.request.build_absolute_uri(product.get_absolute_url()),
                "og_title": product.seo_title or product.name,
                "og_description": product.seo_description or product.short_description,
                "og_image": self.request.build_absolute_uri(main_image.image.url) if main_image else "",
                "og_type": "product",
                "product_schema_json": json.dumps(product_schema, ensure_ascii=False),
            }
        )
        return context


class NewArrivalsView(ProductListView):
    template_name = "catalog/new_arrivals.html"
    page_title = "Новинки Airish Fox"
    meta_description = "Новые товары Airish Fox: свежие вещи, mood-подборки и fox picks."

    def get_queryset(self):
        return active_product_queryset().filter(is_new=True)


class CollectionListView(CatalogContextMixin, ListView):
    template_name = "catalog/collections.html"
    context_object_name = "collections"
    page_title = "Коллекции Airish Fox"
    meta_description = "Fashion-коллекции Airish Fox: seasonal collections, capsules и boutique selections."

    def get_queryset(self):
        return Collection.objects.filter(is_active=True)


class CollectionDetailView(CatalogContextMixin, DetailView):
    model = Collection
    template_name = "catalog/collection_detail.html"
    context_object_name = "collection"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Collection.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = self.object
        context.update(
            {
                "products": active_product_queryset().filter(collections=collection),
                "page_title": collection.seo_title or collection.name,
                "meta_description": collection.seo_description or collection.description,
            }
        )
        context["og_title"] = context["page_title"]
        context["og_description"] = context["meta_description"]
        return context


class MoodDetailView(CatalogContextMixin, DetailView):
    model = MoodCollection
    template_name = "catalog/mood_detail.html"
    context_object_name = "mood"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return MoodCollection.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mood = self.object
        context.update(
            {
                "products": active_product_queryset().filter(moods=mood),
                "page_title": mood.seo_title or mood.name,
                "meta_description": mood.seo_description or mood.description,
            }
        )
        context["og_title"] = context["page_title"]
        context["og_description"] = context["meta_description"]
        return context
