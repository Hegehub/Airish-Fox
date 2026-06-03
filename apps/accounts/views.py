"""Customer account views."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.auth.views import PasswordChangeDoneView as DjangoPasswordChangeDoneView
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.core.ratelimit import check_rate_limit

from .forms import AddressForm, CustomerProfileForm, CustomerRegistrationForm, LoginForm, StyledPasswordChangeForm
from .models import Address, CustomerProfile


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("accounts:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:dashboard")
        if request.method == "POST" and check_rate_limit(request, "register").limited:
            messages.error(request, "Слишком много попыток регистрации. Попробуйте позже.")
            return HttpResponse("Too many registration attempts.", status=429)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Добро пожаловать в Airish Fox. Профиль покупателя создан.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_title": "Регистрация — Airish Fox",
                "meta_description": "Создайте аккаунт покупателя Airish Fox.",
            }
        )
        return context


class LoginView(DjangoLoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and check_rate_limit(request, "login").limited:
            messages.error(request, "Слишком много попыток входа. Попробуйте позже.")
            return HttpResponse("Too many login attempts.", status=429)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Вы вошли в личный кабинет Airish Fox.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_title": "Вход — Airish Fox", "meta_description": "Вход в личный кабинет Airish Fox."})
        return context


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("core:home")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Вы вышли из аккаунта Airish Fox.")
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, DetailView):
    template_name = "accounts/dashboard.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        profile, _created = CustomerProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_title": "Личный кабинет — Airish Fox",
                "meta_description": "Личный кабинет покупателя Airish Fox.",
                "default_shipping_address": self.request.user.addresses.filter(is_default_shipping=True).first(),
                "addresses_count": self.request.user.addresses.count(),
            }
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "accounts/profile_form.html"
    form_class = CustomerProfileForm
    success_url = reverse_lazy("accounts:dashboard")

    def get_object(self, queryset=None):
        profile, _created = CustomerProfile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, "Профиль обновлён.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_title": "Профиль — Airish Fox", "meta_description": "Настройте профиль покупателя Airish Fox."})
        return context


class AddressQuerysetMixin(LoginRequiredMixin):
    model = Address

    def get_queryset(self):
        return self.request.user.addresses.all()


class AddressListView(AddressQuerysetMixin, ListView):
    template_name = "accounts/address_list.html"
    context_object_name = "addresses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_title": "Адреса доставки — Airish Fox", "meta_description": "Адреса доставки покупателя Airish Fox."})
        return context


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = "accounts/address_form.html"
    success_url = reverse_lazy("accounts:address_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Адрес доставки добавлен.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_title": "Новый адрес — Airish Fox", "meta_description": "Добавьте адрес доставки Airish Fox."})
        return context


class AddressUpdateView(AddressQuerysetMixin, UpdateView):
    form_class = AddressForm
    template_name = "accounts/address_form.html"
    success_url = reverse_lazy("accounts:address_list")

    def form_valid(self, form):
        messages.success(self.request, "Адрес доставки обновлён.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_title": "Редактировать адрес — Airish Fox", "meta_description": "Редактирование адреса доставки Airish Fox."})
        return context


class AddressDeleteView(AddressQuerysetMixin, DeleteView):
    template_name = "accounts/address_confirm_delete.html"
    success_url = reverse_lazy("accounts:address_list")

    def form_valid(self, form):
        messages.success(self.request, "Адрес доставки удалён.")
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin, DjangoPasswordChangeView):
    template_name = "accounts/password_change_form.html"
    form_class = StyledPasswordChangeForm
    success_url = reverse_lazy("accounts:password_change_done")

    def form_valid(self, form):
        messages.success(self.request, "Пароль обновлён.")
        return super().form_valid(form)


class PasswordChangeDoneView(LoginRequiredMixin, DjangoPasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"
