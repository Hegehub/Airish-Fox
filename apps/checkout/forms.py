"""Checkout forms."""

from django import forms

from apps.promotions.models import PromoCode
from apps.shipping.models import ShippingMethod
from apps.store_locator.models import StoreLocation

FORM_FIELD_CLASS = "form-control"
CHECKBOX_CLASS = "form-checkbox"


def style_fields(form):
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, forms.CheckboxInput):
            widget.attrs.setdefault("class", CHECKBOX_CLASS)
        else:
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {FORM_FIELD_CLASS}".strip()
    return form


class CheckoutForm(forms.Form):
    full_name = forms.CharField(label="Имя и фамилия", max_length=160)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Телефон", max_length=40)
    shipping_country = forms.CharField(label="Страна", max_length=80, initial="Vietnam")
    shipping_city = forms.CharField(label="Город", max_length=120, required=False)
    shipping_district = forms.CharField(label="Район", max_length=120, required=False)
    shipping_street_address = forms.CharField(label="Адрес", widget=forms.Textarea(attrs={"rows": 3}), required=False)
    shipping_postal_code = forms.CharField(label="Почтовый индекс", max_length=30, required=False)
    shipping_method = forms.ModelChoiceField(label="Способ доставки", queryset=ShippingMethod.objects.none(), empty_label="Выберите доставку")
    pickup_store = forms.ModelChoiceField(label="Магазин самовывоза", queryset=StoreLocation.objects.none(), required=False, empty_label="Выберите магазин")
    promo_code = forms.CharField(label="Промокод", max_length=50, required=False)
    is_gift = forms.BooleanField(label="Это подарок", required=False)
    gift_wrap = forms.BooleanField(label="Подарочная упаковка", required=False)
    gift_message = forms.CharField(label="Подарочное сообщение", max_length=500, widget=forms.Textarea(attrs={"rows": 3, "maxlength": 500}), required=False)
    hide_price_in_package = forms.BooleanField(label="Скрыть цены в посылке", required=False)
    notes = forms.CharField(label="Комментарий", widget=forms.Textarea(attrs={"rows": 3}), required=False)
    website = forms.CharField(label="", required=False, widget=forms.HiddenInput)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["shipping_method"].queryset = ShippingMethod.objects.filter(is_active=True)
        self.fields["pickup_store"].queryset = StoreLocation.objects.filter(is_active=True, pickup_available=True)
        if user and user.is_authenticated:
            self.fields["email"].initial = user.email
            self.fields["full_name"].initial = user.get_full_name() or user.get_username()
            profile = getattr(user, "customer_profile", None)
            if profile:
                self.fields["phone"].initial = profile.phone
            default_address = user.addresses.filter(is_default_shipping=True).first()
            if default_address:
                self.fields["full_name"].initial = default_address.full_name
                self.fields["phone"].initial = default_address.phone
                self.fields["shipping_country"].initial = default_address.country
                self.fields["shipping_city"].initial = default_address.city
                self.fields["shipping_district"].initial = default_address.district
                self.fields["shipping_street_address"].initial = default_address.street_address
                self.fields["shipping_postal_code"].initial = default_address.postal_code
        style_fields(self)

    def clean_promo_code(self):
        code = self.cleaned_data.get("promo_code", "").strip().upper()
        if not code:
            return ""
        try:
            promo = PromoCode.objects.get(code__iexact=code)
        except PromoCode.DoesNotExist as exc:
            raise forms.ValidationError("Промокод не найден.") from exc
        if not promo.is_valid_now():
            raise forms.ValidationError("Промокод недействителен или истёк.")
        return promo.code

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Проверьте данные формы и отправьте заказ ещё раз.")
        shipping_method = cleaned.get("shipping_method")
        if shipping_method and shipping_method.is_store_pickup:
            if self.fields["pickup_store"].queryset.exists() and not cleaned.get("pickup_store"):
                self.add_error("pickup_store", "Выберите магазин для самовывоза.")
            return cleaned
        if not cleaned.get("shipping_city"):
            self.add_error("shipping_city", "Укажите город доставки.")
        if not cleaned.get("shipping_street_address"):
            self.add_error("shipping_street_address", "Укажите адрес доставки.")
        return cleaned
