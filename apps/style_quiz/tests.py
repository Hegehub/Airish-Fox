from django.test import TestCase
from django.urls import reverse
from apps.catalog.models import Category, MoodCollection
from .models import StyleQuizOption, StyleQuizQuestion, StyleQuizSubmission

class StyleQuizTests(TestCase):
    def setUp(self):
        self.mood = MoodCollection.objects.create(name="Mint Mood", slug="mint")
        self.category = Category.objects.create(name="Dresses", slug="dresses")
        self.question = StyleQuizQuestion.objects.create(title="Настроение?", slug="mood")
        self.option = StyleQuizOption.objects.create(question=self.question, label="Mint", value="mint", mood=self.mood, category=self.category)
    def test_quiz_page_returns_200(self):
        response = self.client.get(reverse("style_quiz:start"))
        self.assertEqual(response.status_code, 200)
    def test_submission_saves_and_redirects(self):
        response = self.client.post(reverse("style_quiz:start"), {f"question_{self.question.pk}": self.option.pk})
        self.assertEqual(response.status_code, 302)
        self.assertIn("mood=mint", response["Location"])
        submission = StyleQuizSubmission.objects.get()
        self.assertIn("mood=mint", submission.result_url)
