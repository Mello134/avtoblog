from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('category/<int:category_id>/', categories, name="category"),
    path('car/<int:car_id>/', car, name='car'),
]