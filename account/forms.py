from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # стандартные формы django
from django.contrib.auth.models import User  # из djando достаём записи модели User (все пользователи)
from django import forms  # модуль forms - для написания полей


# форма регистрации
class RegisterUserForm(UserCreationForm):
    # прописываем все необходимые поля, самостоятельно
    # тк django в meta их не видит почему-то без этого
    # название полей можно посмотреть в коде html - или в документации
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User  # связываемся с моделью User
        # отображаем поля модели User
        fields = ('username', 'email', 'password1', 'password2')


# Форма авторизации
class LoginUserForm(AuthenticationForm):  # AuthenticationForm - стандартная форма
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form.input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form.input'}))

