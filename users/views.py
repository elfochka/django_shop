from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import CreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy


class AccountDetailView(TemplateView):
    template_name = 'users/account.html'


class RegisterView(FormView):
    form_class = CreationForm
    success_url = reverse_lazy('users:account')
    template_name = "users/registration.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# def register(request):
#     if request.method == 'POST':
#         user_form = CreationForm(request.POST)
#         print(user_form.data)
#         user_form.save()
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(user_form.cleaned_data['pass'])
#             new_user.save()
#             print("all ok")
#             return render(request, "../templates/users/account.html")
#     else:
#         user_form = CreationForm()
#     return render(request, "../templates/users/registration.html")

# class CustomAuthenticationForm(AuthenticationForm):
#     email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
#
# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'password1', 'password2')

# class LoginView(TemplateView):
#     template_name = "users/login.html"


class EmailView(TemplateView):
    template_name = "users/e-mail.html"


class PasswordView(TemplateView):
    template_name = "users/password.html"


class ProfileView(TemplateView):
    template_name = "users/profile.html"


class UserProfileUpdateForm(TemplateView):
    template_name = "users/profile_update.html"


class ActionListView(TemplateView):
    template_name = "users/viewhistory.html"
