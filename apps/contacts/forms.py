from django import forms

from .models import ContactRequest


class ContactRequestForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'tabindex': '-1', 'class': 'honeypot-field'}))

    class Meta:
        model = ContactRequest
        fields = ('name', 'phone', 'email', 'preferred_contact_method', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 999 000-00-00'}),
            'email': forms.EmailInput(attrs={'placeholder': 'hello@example.com'}),
            'message': forms.Textarea(attrs={'placeholder': 'Расскажите, какой образ вы ищете', 'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('preferred_contact_method')
        phone = cleaned_data.get('phone')
        email = cleaned_data.get('email')
        if method in {'phone', 'email'} and not phone and not email:
            raise forms.ValidationError('Укажите телефон или email для связи.')
        return cleaned_data

    @property
    def is_honeypot_filled(self):
        return bool(self.data.get('website'))
