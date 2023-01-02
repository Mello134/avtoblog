from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from blog.utils import DataMixin
from video.forms import VideoYouTubeRuTubeForm, VideoYouTubeRuTubeUpdateForm
from video.models import VideoYouTubeRuTube

"""Всё что связано с реакциями на отдельное видео (лайки, закладки, комментарии)
Смотри video_tags - все функции там, так как реализация через вложенные теги шаблонов"""


# представление шаблона со списком видео
class AllVideoListShow(ListView):
    # paginate_by = 4 пагинация на будущее
    model = VideoYouTubeRuTube
    template_name = 'video/video_list.html'
    context_object_name = 'video'  # objects = video (для обращения в шаблоне)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # в контексте сейчас только форма, объект
        context['title'] = 'Все видео'
        context['sidebar_selected'] = 'all'
        return {**context}


# представление для создания видеопоста
class AddVideo(CreateView):
    model = VideoYouTubeRuTube  # модель объекта (может быть и не нужна)
    template_name = 'video/video_add.html'  # шаблон
    form_class = VideoYouTubeRuTubeForm  # наша форма
    success_url = reverse_lazy('video_all')  # перенаправление после обработки формы

    # переопределяем метод form_valid (для того чтобы автор автоматом заполнился)
    def form_valid(self, form):  # берём форму
        self.object = form.save(commit=False)  # когда нужно что-то подкорректировать автоматом
        self.object.author_video = self.request.user  # записываю в поле автор авторизованного пользователя (автоматом)
        self.object.save()  # форма пересохраняется с новыми данными
        return super().form_valid(form)  # форма передаётся в базу данных и программа продолжит свои действия

    # переопределяю (добавляю в контекст свою информацию)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # распаковываем изначальный контекст
        context['title'] = 'Добавление видео c YouTube или Rutube'  # добавил title в контекст
        return {**context}  # передаю весь распакованный контекст


# представление для редактирования видеопоста (только поле имя поста)
class UpdateVideo(UpdateView):
    model = VideoYouTubeRuTube
    form_class = VideoYouTubeRuTubeUpdateForm
    pk_url_kwarg = 'pk_video'  # переопределили, стандартно: [pk_url_kwarg = "pk"]
    template_name = 'video/video_update.html'
    success_url = reverse_lazy('video_all')  # перенаправление после обработки формы

    # добавляю в контекст свои параметры
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # в контексте сейчас только форма, объект
        context['title'] = 'Редактирование видеопоста'
        return {**context}


# представление для удаления видеопоста
class DeleteVideo(DeleteView):
    model = VideoYouTubeRuTube
    template_name = 'video/video_delete.html'
    pk_url_kwarg = 'pk_video'  # переопределили, стандартно: [pk_url_kwarg = "pk"]
    success_url = reverse_lazy('video_all')  # перенаправление после обработки формы

    # добавляю в контекст свои параметры
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # в контексте сейчас только форма, объект
        context['title'] = 'Удаление видеопоста'
        return {**context}


