from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('category/<int:category_id>/', categories, name="category"),
    path('car/<slug:car_slug>/', car, name='car'),
]