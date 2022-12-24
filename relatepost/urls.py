from django.urls import path
from .views import *

urlpatterns = [
    path('add-rating/', AddStarRating.as_view(), name='add_rating'),
    path('category/<slug:cat_slug>/<slug:car_slug>/like', like_post, name='like_post'),
]

