from django.shortcuts import render
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





