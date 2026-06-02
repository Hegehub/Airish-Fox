from django.contrib import admin
from .models import StyleQuizOption, StyleQuizQuestion, StyleQuizSubmission

class StyleQuizOptionInline(admin.TabularInline):
    model = StyleQuizOption
    extra = 1

@admin.register(StyleQuizQuestion)
class StyleQuizQuestionAdmin(admin.ModelAdmin):
    inlines = (StyleQuizOptionInline,)
    list_display = ("title", "slug", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("title", "help_text")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_active", "sort_order")

@admin.register(StyleQuizOption)
class StyleQuizOptionAdmin(admin.ModelAdmin):
    list_display = ("label", "question", "value", "mood", "category", "gift_intent", "is_active", "sort_order")
    list_filter = ("is_active", "gift_intent", "question")
    search_fields = ("label", "value")

@admin.register(StyleQuizSubmission)
class StyleQuizSubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "session_key", "result_url", "created_at")
    search_fields = ("user__username", "session_key", "result_url")
    readonly_fields = ("user", "session_key", "answers", "result_url", "created_at")
