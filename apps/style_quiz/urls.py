from django.urls import path
from .views import StyleQuizResultsView, StyleQuizView
app_name = "style_quiz"
urlpatterns = [path("", StyleQuizView.as_view(), name="start"), path("results/", StyleQuizResultsView.as_view(), name="results")]
