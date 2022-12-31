from django.views.generic import ListView
from blog.utils import DataMixin
from video.models import VideoYouTubeRuTube

"""Всё что связано с реакциями на отдельное видео (лайки, закладки, комментарии)
Смотри video_tags - все функции там, так как реализация через вложенные теги шаблонов"""


# представление шаблона со списком видео
class AllVideoListShow(DataMixin, ListView):
    # paginate_by = 8 пагинация на будущее
    model = VideoYouTubeRuTube
    template_name = 'video/video_list.html'
    context_object_name = 'video'  # objects = video (для обращения в шаблоне)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Все видео')
        return {**context, **c_def}
