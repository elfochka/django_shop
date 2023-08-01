from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from users.models import CustomUser


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'password1')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
