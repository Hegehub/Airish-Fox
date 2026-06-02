"""Fox Style Quiz views."""
from urllib.parse import urlencode
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from apps.brand.services import is_feature_enabled
from .models import StyleQuizQuestion, StyleQuizSubmission

class StyleQuizView(View):
    template_name = "style_quiz/start.html"

    def get_questions(self):
        return StyleQuizQuestion.objects.filter(is_active=True).prefetch_related("options", "options__mood", "options__category")

    def get(self, request):
        return render(request, self.template_name, {"questions": self.get_questions(), "page_title": "Fox Style Quiz — Airish Fox", "meta_description": "Простой quiz Airish Fox подбирает mood, цвет и gift-ready подборку без AI."})

    def post(self, request):
        if not is_feature_enabled("style_quiz_enabled", True):
            return redirect("catalog:product_list")
        questions = self.get_questions()
        answers = {}
        params = {}
        for question in questions:
            option_id = request.POST.get(f"question_{question.pk}")
            if not option_id:
                continue
            option = question.options.filter(pk=option_id, is_active=True).first()
            if not option:
                continue
            answers[question.slug] = {"label": option.label, "value": option.value}
            if option.mood_id and "mood" not in params:
                params["mood"] = option.mood.slug
            if option.category_id and "category" not in params:
                params["category"] = option.category.slug
            if option.preferred_color_hex and "color" not in params:
                params["color"] = option.preferred_color_hex.lstrip("#")
            if option.gift_intent:
                params["gift_ready"] = "1"
        result_url = reverse("catalog:product_list")
        if params:
            result_url = f"{result_url}?{urlencode(params)}"
        if not request.session.session_key:
            request.session.save()
        StyleQuizSubmission.objects.create(user=request.user if request.user.is_authenticated else None, session_key=request.session.session_key or "", answers=answers, result_url=result_url)
        request.session["style_quiz_result_url"] = result_url
        return redirect(result_url)

class StyleQuizResultsView(View):
    def get(self, request):
        result_url = request.session.get("style_quiz_result_url") or reverse("catalog:product_list")
        return render(request, "style_quiz/results.html", {"result_url": result_url, "page_title": "Ваша подборка — Airish Fox", "meta_description": "Результат Fox Style Quiz."})
