from django.http import HttpResponse
from django.shortcuts import render


# домашняя страница
def home(request):
    context = {
        'title': 'Главная страница',
        'key_2': 'Значение 2',
    }
    return render(request, 'blog/home.html', context=context)


# страница категорий
def categories(request, category_id):  # в скобках то что получаем в запросе
    # в return то что отдаём для отображения
    print(request.GET)
    return HttpResponse(f'<h1>Страница категорий</h1><p>№ {category_id}</p>')


# страница отдельной машины
def car(request, car_id):
    return HttpResponse(f'<h1>Страница отдельной машины</h1><p>№ { car_id }</p>')


# Create your views here.
