from django.urls import path

from .templatetags.video_tags import show_all_ralations_to_video, like_video, bookmarks_video, like_button_comment_video
from .views import *

urlpatterns = [
    path('all/', AllVideoListShow.as_view(), name="video_all"),

    # show_all_ralations_to_video - Это вложенный тег (шаблон all_ralations_to_video),
    # В ней находится вывод и обработка формы для комментариев
    # по этому для добавления комментария нужно вызвать эту функцию = вложенный шаблон.
    path('add_comment/<int:pk_video>/', show_all_ralations_to_video, name='add_comment'),  # Добавить комментарий к видео
    path('like_comment/<int:pk_com>/', like_button_comment_video, name='like_comment'),  # Лайк комментария

    path('like_video/<int:pk_video>/', like_video, name='like_video'),  # ЛАЙК ВИДЕО
    path('bookmarks_video/<int:pk_video>/', bookmarks_video, name='bookmarks_video'),  # ЗАКЛАДКА ВИДЕО
]
