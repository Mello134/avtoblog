from django.http import HttpResponse
from django.shortcuts import render
from .models import *


# домашняя страница
def home(request):
    cars = Car.objects.all()
    context = {
        'title': 'Все модели',
        'cars': cars,
    }
    return render(request, 'blog/home.html', context=context)

# страница категорий
def categories(request, category_id):  # в скобках то что получаем в запросе
    # в return то что отдаём для отображения
    print(request.GET)
    return HttpResponse(f'<h1>Страница категорий</h1><p>№ {category_id}</p>')


# страница отдельной машины
def car(request, car_slug):
    car = Car.objects.get(slug=car_slug)
    context = {
        'car': car,
    }
    return render(request, 'blog/car.html', context=context)


# Create your views here.
