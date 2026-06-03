"""Simple non-AI style quiz models."""
from django.conf import settings
from django.db import models

class StyleQuizQuestion(models.Model):
    title = models.CharField("Вопрос", max_length=180)
    slug = models.SlugField("Slug", unique=True)
    help_text = models.CharField("Подсказка", max_length=255, blank=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    class Meta:
        verbose_name = "Style quiz question"
        verbose_name_plural = "Style quiz questions"
        ordering = ["sort_order", "title"]
    def __str__(self): return self.title

class StyleQuizOption(models.Model):
    question = models.ForeignKey(StyleQuizQuestion, related_name="options", on_delete=models.CASCADE, verbose_name="Вопрос")
    label = models.CharField("Label", max_length=140)
    value = models.CharField("Value", max_length=80)
    mood = models.ForeignKey("catalog.MoodCollection", null=True, blank=True, on_delete=models.SET_NULL, related_name="quiz_options", verbose_name="Mood")
    category = models.ForeignKey("catalog.Category", null=True, blank=True, on_delete=models.SET_NULL, related_name="quiz_options", verbose_name="Категория")
    preferred_color_hex = models.CharField("Цвет", max_length=7, blank=True)
    gift_intent = models.BooleanField("Подарок", default=False)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    class Meta:
        verbose_name = "Style quiz option"
        verbose_name_plural = "Style quiz options"
        ordering = ["sort_order", "label"]
    def __str__(self): return self.label

class StyleQuizSubmission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="style_quiz_submissions")
    session_key = models.CharField("Session key", max_length=80, blank=True)
    answers = models.JSONField("Answers", default=dict)
    result_url = models.CharField("Result URL", max_length=500)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    class Meta:
        verbose_name = "Style quiz submission"
        verbose_name_plural = "Style quiz submissions"
        ordering = ["-created_at"]
    def __str__(self): return self.result_url
