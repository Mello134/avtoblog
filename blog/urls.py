from django.urls import path
from .views import *

urlpatterns = [
    path('', show_home, name='home'),
    path('category/<slug:cat_slug>/', show_categories, name="category"),
    path('category/<slug:cat_slug>/<slug:car_slug>', show_car, name='car'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]

# cat_slug
# path('car/<slug:car_slug>/', show_car, name='car'),