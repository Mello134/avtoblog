from django.urls import path
from .views import *

urlpatterns = [
    path('add-rating/', AddStarRating.as_view(), name='add_rating'),
]

