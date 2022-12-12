from django.urls import path
from .views import *

urlpatterns = [
    path('', CarsAllShow.as_view(), name='home'),
    path('category/<slug:cat_slug>/', CarsCategoryShow.as_view(), name="category"),
    path('category/<slug:cat_slug>/<slug:car_slug>/', ShowCar.as_view(), name='car'),
    path('add_post/', show_add_post, name='add_post'),
    path('category/<slug:cat_slug>/<slug:car_slug>/update/', UpdatePostView.as_view(), name='update_post'),
    path('category/<slug:cat_slug>/<slug:car_slug>/delete/', DeletePostView.as_view(), name='delete_post'),
]

