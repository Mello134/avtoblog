from django.contrib.auth import logout, login
from django.contrib.auth.models import User  # модель User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.forms import RegisterUserForm, LoginUserForm
from blog.utils import DataMixin


# Create your views here.
# класс представления RegisterUser
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm  # наша форма из forms.py
    template_name = 'account/register.html'  # шаблон куда передаём
    success_url = reverse_lazy('login')  # При успешной регистрации направит path 'login'

    # формируем полный словарь context
    def get_context_data(self, object_list=None, **kwargs):
        # берём контекст из этого класса представления
        context = super().get_context_data(**kwargs)  # на данный момент form_class
        # берём контекст из DataMixin - и в него сразу добавляем title
        c_def = self.get_user_context(title='Регистрация')
        # передаём в шаблон общий контекст (RegisterUser + DataMixin)
        return {**context, **c_def}
        # или
        # return dict(list(context.items()) + list(c_def.items()))

    # автозалогинивание при успешной регистрации
    def form_valid(self, form):
        user = form.save()  # сохраняем данные пользователя в БД (User)
        login(self.request, user)  # авторизовывает пользователя
        return redirect('home')  # перенаправляет домой


# Класс представления формы авторизации
# Логика работы базового класса LoginView + сама форма LoginUserForm
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm  # наша форма из forms.py
    template_name = 'account/login.html'  # шаблон

    # формируем полный контекст
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # распаковываем изначальный контекст
        c_def = self.get_user_context(title='Авторизация')  # переменная контекста DataMixin
        return {**context, **c_def}  # в шаблон передаём полный контекст

    def get_success_url(self):
        return reverse_lazy('home')  # при успешном входе перенаправит домой


# выход из аккаунта
def logout_user(request):
    logout(request)  # стандартный выход пользователя
    return redirect('login')  # перенаправляет залогиниться


# просмотр информации о пользователе
def show_profile(request):
    current_user = request.user

    user_info = User.objects.get(username=current_user)

    all_user = User.objects.all()
    context = {
        'all_user': all_user,
        'current_user': current_user,
        'user_info': user_info,
    }
    return render(request, 'account/profile.html', context=context)