from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView, UpdateView

from orders.models import Order
from users.forms import CustomUserChangeForm
from users.models import Action, CustomUser


class AccountDetailView(LoginRequiredMixin, TemplateView):
    template_name = "users/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["latest_order"] = Order.objects.filter(client_id=self.request.user).order_by("-created").first()
        context["actions"] = Action.objects.filter(verb=Action.VIEW_PRODUCT, user=self.request.user)[:3]
        return context


class EmailView(TemplateView):
    template_name = "users/e-mail.html"

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        last_request_time = cache.get(f"last_request_{email}")

        user_exists = CustomUser.objects.filter(email=email).exists()
        if not user_exists:
            request.session["time_limit_error"] = "Введенный e-mail не найден."
            return HttpResponseRedirect(reverse("users:e-mail"))

        if last_request_time and (timezone.now() - last_request_time).total_seconds() < 60:
            request.session["time_limit_error"] = "Вы не можете запрашивать проверочный код чаще одного раза в минуту."
            return HttpResponseRedirect(reverse("users:e-mail"))

        reset_code = get_random_string(length=6, allowed_chars="0123456789")
        reset_url = request.build_absolute_uri(f"{reverse('users:password')}?code={reset_code}")

        cache.set(f"email_for_code_{reset_code}", email, 3600)
        cache.set(f"reset_code_{email}", reset_code, 3600)
        cache.set(f"last_request_{email}", timezone.now(), 3600)

        send_mail(
            "Восстановление пароля",
            f"Ваш код для восстановления пароля: {reset_code}\n"
            f"Или перейдите по ссылке: {reset_url}",
            "from@example.com",
            [email],
            fail_silently=False,
        )

        if "time_limit_error" in request.session:
            del request.session["time_limit_error"]

        return HttpResponseRedirect(reverse("users:email_sent"))


class EmailSentView(TemplateView):
    template_name = "users/e-mail_sent.html"


class PasswordView(TemplateView):
    template_name = "users/password.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = self.request.GET.get("code")
        context["code"] = code
        return context

    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        email = cache.get(f"email_for_code_{code}")

        if email and cache.get(f"reset_code_{email}") == code:
            return super().get(request, *args, **kwargs)
        else:
            return JsonResponse({"status": "error", "message": "Invalid or expired code."})

    def post(self, request, *args, **kwargs):
        new_password = request.POST.get("pass")
        code = request.GET.get("code")
        email = cache.get(f"email_for_code_{code}")

        if email and cache.get(f"reset_code_{email}") == code:
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)  # Используем set_password для безопасности
            user.save()

            cache.delete(f"reset_code_{email}")
            cache.delete(f"email_for_code_{code}")

            return HttpResponseRedirect(reverse("account_login"))
        else:
            return JsonResponse({"status": "error", "message": "Invalid or expired code."})


class HistoryOrderView(TemplateView):
    template_name = "users/historyorder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["orders"] = Order.objects.filter(client_id=self.request.user)

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:account")

    def get_initial(self):
        initial = super().get_initial()
        initial["full_name"] = self.request.user.get_full_name()
        return initial


class ActionListView(LoginRequiredMixin, TemplateView):
    template_name = "users/viewhistory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actions"] = Action.objects.filter(verb=Action.VIEW_PRODUCT, user=self.request.user)[:20]
        return context
