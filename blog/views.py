from django.shortcuts import render, redirect, get_object_or_404
from .forms import CarAddForm
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


def show_add_post(request):
    if request.method == 'POST':  # если уже введены какие-то данные
        # request.FILES - Обязательно если есть файлы, изображения и ТД
        form = CarAddForm(request.POST, request.FILES)  # форма = заполненная форма
        if form.is_valid():  # проверка правильности формы, если форма заполнена правильно
            form.save()  # сохраняет запись в БД
            return redirect('home')  # перенаправление домой при успешном заполнении
    else:  # если никаких данный пользователь ещё не вводил
        form = CarAddForm()  # отображаем пустую форму для заполнения

    context = {
          'title': 'Добавление статьи',
          'all_categories': all_categories,
          'form': form,
      }
    return render(request, 'blog/add_post.html', context=context)


