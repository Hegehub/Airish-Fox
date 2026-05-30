from django.views.generic import ListView

from .models import Category, Product


class CollectionView(ListView):
    model = Product
    template_name = 'pages/collection.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')
        self.current_category = None
        category_slug = self.request.GET.get('category')
        if category_slug:
            self.current_category = Category.objects.filter(slug=category_slug, is_active=True).first()
            if self.current_category:
                queryset = queryset.filter(category=self.current_category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Коллекция Airish Fox',
            'meta_description': 'Мини-витрина одежды Airish Fox: категории, размеры, цвета и актуальные модели.',
            'categories': Category.objects.filter(is_active=True),
            'current_category': self.current_category,
        })
        return context


class NewArrivalsView(ListView):
    model = Product
    template_name = 'pages/new_arrivals.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_active=True, is_new=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Новинки Airish Fox',
            'meta_description': 'Свежие поступления Airish Fox: новые fashion-модели в mint и orange настроении.',
        })
        return context
