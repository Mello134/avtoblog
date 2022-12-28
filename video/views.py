from django.shortcuts import render
from django.views.generic import ListView
from blog.utils import DataMixin
from video.models import VideoYouTubeRuTube


# представление шаблона со списком видео
class AllVideoListShow(DataMixin, ListView):
    # paginate_by = 8 пагинация на будущее
    model = VideoYouTubeRuTube
    template_name = 'video/video_all.html'
    context_object_name = 'video'  # objects = video (для обращения в шаблоне)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Все видео')
        return {**context, **c_def}
