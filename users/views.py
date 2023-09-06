from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.generic import ListView, TemplateView, UpdateView

from users.forms import CustomUserChangeForm
from users.models import Action, CustomUser


class AccountDetailView(LoginRequiredMixin, TemplateView):
    template_name = "users/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class EmailView(TemplateView):
    template_name = "users/e-mail.html"

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        last_request_time = cache.get(f"last_request_{email}")

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

        return HttpResponseRedirect(reverse("users:verify_code"))


class VerifyCodeView(TemplateView):
    template_name = "users/verify_code.html"

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        code = request.POST.get("code")
        cached_code = cache.get(f"reset_code_{email}")

        if code == cached_code:
            redirect_url = f"{reverse('users:password')}?code={code}"
            return HttpResponseRedirect(redirect_url)
        else:
            request.session["verification_error"] = "Invalid verification code."
            return HttpResponseRedirect(reverse("users:verify_code"))


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


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:account")

    def get_initial(self):
        initial = super().get_initial()
        initial["full_name"] = self.request.user.get_full_name()
        return initial


class ActionListView(LoginRequiredMixin, ListView):
    model = Action
    template_name = "users/viewhistory.html"
    queryset = Action.objects.filter(verb=Action.VIEW_PRODUCT)
    context_object_name = "actions"

    def get_queryset(self):
        """
        Get last 20 product views for authenticated user.
        """
        return self.queryset.filter(user=self.request.user)[:20]
