from django.urls import path
from .views import *

urlpatterns = [
    path('', show_home, name='home'),
    path('category/<slug:cat_slug>/', show_categories, name="category"),
    path('category/<slug:cat_slug>/<slug:car_slug>/', show_car, name='car'),
    path('add_post/', show_add_post, name='add_post'),
    path('category/<slug:cat_slug>/<slug:car_slug>/update/', UpdatePostView.as_view(), name='update_post'),
    path('category/<slug:cat_slug>/<slug:car_slug>/delete/', DeletePostView.as_view(), name='delete_post'),
]

