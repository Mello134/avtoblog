from django.contrib.auth import logout, login  # выход/вход пользователя django
from django.contrib.auth.forms import UserCreationForm  # форма django
from django.contrib.auth.views import LoginView  # стандартная логика авторизации
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy  # перенаправление на маршрут
from django.views.generic import CreateView  # класс представления

from .forms import *  # наш forms.py
from .utils import DataMixin  # наш Mixin
from .models import *
from django.core.paginator import Paginator


all_categories = Category.objects.all()


# домашняя страница
def show_home(request):
    cars = Car.objects.all().order_by('?')  # каждое обновление рандомный порядок

    paginator = Paginator(cars, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'cat_selected': 'all',
        'all_categories': all_categories,
        'title': 'Все модели',
        # 'cars': cars,
    }
    return render(request, 'blog/home.html', context=context)


# вывод записей Car - по выбранной категории
def show_categories(request, cat_slug):  # в скобках то что получаем в запросе
    # cat__slug - обращение из модели Car - к полю slug модели Category
    # cat_slug - значение поля slug - выбранной категории - см get_abs_url Category
    cars = Car.objects.filter(cat__slug=cat_slug)
    category_1 = Category.objects.get(slug=cat_slug)

    paginator = Paginator(cars, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'all_categories': all_categories,
        'cat_selected': cat_slug,
        'title': f'Производство: {category_1}',
        # 'cars': cars,
    }
    return render(request, 'blog/home.html', context=context)


# страница отдельной машины
def show_car(request, car_slug, cat_slug):
    car = Car.objects.get(slug=car_slug)
    context = {
        'cat_selected': cat_slug,
        'all_categories': all_categories,
        'car': car,
    }
    return render(request, 'blog/car.html', context=context)


# класс представления RegisterUser
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm  # наша форма из forms.py
    template_name = 'blog/register.html'  # шаблон куда передаём
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
    template_name = 'blog/login.html'  # шаблон

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


