from django.urls import path

from .templatetags.video_tags import show_comments_and_form_comment_self_video
from .views import *

urlpatterns = [
    path('all/', AllVideoListShow.as_view(), name="video_all"),

    # путь на добавление комментария, для запуска функции, в нашем случае тега show_comments_and_form_comment_self_video
    path('add-comment/<int:pk_video>/', show_comments_and_form_comment_self_video, name='add_comment')
]
