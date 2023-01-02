from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from blog.utils import DataMixin
from video.forms import VideoYouTubeRuTubeForm, VideoYouTubeRuTubeUpdateForm
from video.models import VideoYouTubeRuTube, LikeMarkVideo

"""Всё что связано с реакциями на отдельное видео (лайки, закладки, комментарии)
Смотри video_tags - все функции там, так как реализация через вложенные теги шаблонов"""


# представление шаблона со списком видео (все видео)
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


# представление шаблона со списком видео (добавленных в закладки пользователем)
class BookmarksVideoListShow(LoginRequiredMixin, ListView):
    login_url = 'login'  # перенаправление если пользователь не авторизован (LoginRequiredMixin)
    model = VideoYouTubeRuTube
    template_name = 'video/video_list.html'
    context_object_name = 'video'  # objects = video (для обращения в шаблоне)
    # allow_empty = True - покажет пустой список если ничего не будет
    # allow_empty = False - покажет 404, при отсутствии совпадений в get_queryset
    allow_empty = True  # для отображения 404

    # параметры вывода (выводим записи видео только из, закладок пользователя)
    def get_queryset(self):
        # список записей модели LikeMarkVideo (пользователь=request пользователь, стоит в закладках)
        bookmarks_video_list = LikeMarkVideo.objects.filter(user_lm_video__pk=self.request.user.pk,
                                                            is_bookmarks_video=True)
        pk_list_bookmarks_for_user = []  # создал пустой список
        # перебираю все записи по нужным параметрам для пользователя
        for one_rec in bookmarks_video_list:
            # в созданный список, добавляю pk записей, на каждой итерации цикла
            # по итогу будет список всех необходимых pk
            pk_list_bookmarks_for_user.append(one_rec.video_lm.pk)
        # Вывожу только записи из закладок
        # pk - это VideoYouTubeRuTube.pk,
        # __in - необходим когда атрибутов одного поля несколько (список значений одного аттрибута)
        # пример = Model.objects.filter(цвет__in=['белый','чёрный','синий'])
        return VideoYouTubeRuTube.objects.filter(pk__in=pk_list_bookmarks_for_user)

    # добавляю свои параметры в контекст, для передачи в шаблон
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавленные видео'
        context['sidebar_selected'] = 'bookmarks'
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


