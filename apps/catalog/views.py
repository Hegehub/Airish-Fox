from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Category, MoodCollection, Product


class CollectionView(ListView):
    model = Product
    template_name = 'pages/collection.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('moods')
        self.current_category = None
        self.current_mood = None
        category_slug = self.request.GET.get('category')
        mood_slug = self.request.GET.get('mood')
        if category_slug:
            self.current_category = Category.objects.filter(slug=category_slug, is_active=True).first()
            if self.current_category:
                queryset = queryset.filter(category=self.current_category)
        if mood_slug:
            self.current_mood = MoodCollection.objects.filter(slug=mood_slug, is_active=True).first()
            if self.current_mood:
                queryset = queryset.filter(moods=self.current_mood)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Коллекция Airish Fox',
            'meta_description': 'Мини-витрина одежды Airish Fox: категории, mood-подборки, размеры, цвета и актуальные модели.',
            'canonical_path': self.request.path,
            'categories': Category.objects.filter(is_active=True),
            'moods': MoodCollection.objects.filter(is_active=True),
            'current_category': self.current_category,
            'current_mood': self.current_mood,
        })
        return context


class NewArrivalsView(ListView):
    model = Product
    template_name = 'pages/new_arrivals.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_active=True, is_new=True, available=True).select_related('category').prefetch_related('moods')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Новинки Airish Fox',
            'meta_description': 'Свежие поступления Airish Fox: новые fashion-модели в mint и orange настроении.',
            'canonical_path': self.request.path,
        })
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category').prefetch_related('moods', 'images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        mood_ids = product.moods.values_list('id', flat=True)
        related = Product.objects.filter(is_active=True, available=True).exclude(id=product.id).filter(
            Q(category=product.category) | Q(moods__in=mood_ids)
        ).select_related('category').prefetch_related('moods').distinct()[:4]
        context.update({
            'page_title': f'{product.name} — Airish Fox',
            'meta_description': product.short_description,
            'canonical_path': product.get_absolute_url(),
            'og_image': product.main_image.url if product.main_image else '',
            'related_products': related,
        })
        return context
