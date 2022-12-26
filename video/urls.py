from django.urls import path
from .views import *

urlpatterns = [
    path('all/', AllVideoListShow.as_view(), name="video_all"),
]
