from django import forms

from .models import ContactRequest


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ('name', 'phone', 'email', 'preferred_contact_method', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 999 000-00-00'}),
            'email': forms.EmailInput(attrs={'placeholder': 'hello@example.com'}),
            'message': forms.Textarea(attrs={'placeholder': 'Расскажите, какой образ вы ищете', 'rows': 5}),
        }
