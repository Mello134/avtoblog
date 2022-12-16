from django.urls import path
from comments.views import like_button_comment, delete_button_comment

urlpatterns = [
    path('category/<slug:cat_slug>/<slug:car_slug>/<int:com_id>/', like_button_comment, name='like_button_comment'),
    path('category/<slug:cat_slug>/<slug:car_slug>/<int:com_id>/delete_comment',
         delete_button_comment,
         name='delete_comment'),

]
