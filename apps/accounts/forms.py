"""Forms for customer authentication, profiles and addresses."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Address, CustomerProfile

FORM_FIELD_CLASS = "form-control"
CHECKBOX_CLASS = "form-checkbox"


def style_form_fields(form):
    """Apply Airish Fox form classes to regular fields and checkboxes."""
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, forms.CheckboxInput):
            widget.attrs.setdefault("class", CHECKBOX_CLASS)
        else:
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {FORM_FIELD_CLASS}".strip()
    return form


class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form_fields(self)
        self.fields["username"].label = "Логин"

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomerProfileForm(forms.ModelForm):
    birthday = forms.DateField(
        required=False,
        label="Дата рождения",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = CustomerProfile
        fields = (
            "phone",
            "birthday",
            "preferred_size_top",
            "preferred_size_bottom",
            "preferred_fit",
            "favorite_color",
            "favorite_mood",
            "marketing_consent",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form_fields(self)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "full_name",
            "phone",
            "country",
            "city",
            "district",
            "ward",
            "street_address",
            "postal_code",
            "delivery_notes",
            "is_default_shipping",
        )
        widgets = {
            "street_address": forms.Textarea(attrs={"rows": 3}),
            "delivery_notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form_fields(self)


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        style_form_fields(self)
        self.fields["username"].label = "Логин"
        self.fields["password"].label = "Пароль"


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        style_form_fields(self)
