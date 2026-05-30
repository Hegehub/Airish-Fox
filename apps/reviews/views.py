from django.views.generic import ListView

from .models import Review


class ReviewsView(ListView):
    model = Review
    template_name = 'pages/reviews.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Отзывы Airish Fox',
            'meta_description': 'Отзывы клиентов о стиле, качестве и настроении одежды Airish Fox.',
            'canonical_path': self.request.path,
        })
        return context
