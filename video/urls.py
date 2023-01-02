from django.urls import path

from .templatetags.video_tags import show_all_ralations_to_video, like_video, bookmarks_video, \
    like_button_comment_video, delete_comment_video_button
from .views import *

urlpatterns = [
    path('all/', AllVideoListShow.as_view(), name="video_all"),  # отображение всех видео
    path('bookmarks/', BookmarksVideoListShow.as_view(), name='video_bookmarks'),  # отображение списка по закладкам
    path('my/', MyVideoListShow.as_view(), name='video_my'),  # отображение собственных видео


    path('video_add/', AddVideo.as_view(), name='video_add'),  # Добавление видео
    path('video_update/<int:pk_video>/', UpdateVideo.as_view(), name='video_update'),  # Обновить видео пост
    path('video_delete/<int:pk_video>/', DeleteVideo.as_view(), name='video_delete'),  # Удалить видео

    # show_all_ralations_to_video - Это вложенный тег (шаблон all_ralations_to_video),
    # В ней находится вывод и обработка формы для комментариев
    # по этому для добавления комментария нужно вызвать эту функцию = вложенный тег шаблона.
    path('add_comment/<int:pk_video>/', show_all_ralations_to_video, name='add_comment'),  # Добавить комментарий к видео
    path('like_comment/<int:pk_com>/', like_button_comment_video, name='like_comment'),  # Лайк комментария
    path('delete_comment/<int:pk_com>/', delete_comment_video_button, name='delete_comment'),  # удалить коммент к видео
    path('like_video/<int:pk_video>/', like_video, name='like_video'),  # ЛАЙК ВИДЕО
    path('bookmarks_video/<int:pk_video>/', bookmarks_video, name='bookmarks_video'),  # ЗАКЛАДКА ВИДЕО
]
