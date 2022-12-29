from django import template
from django.contrib import messages
from django.shortcuts import redirect

from video.forms import CommentVideoYtRtForm
from video.models import VideoYouTubeRuTube, CommentVideoYtRt

# регистрируем этот файл в библиотеке
register = template.Library()


# тег получение формы комментария + самих комментариев для каждого видео (в списке видео)
@register.inclusion_tag('video/comments_and_comment_form_self_video.html')  # в скобках шаблон тега
# pk_video - (необходимо будет указывать в шаблоне, при вызове тега, думаю в цикле)
# pk_video в шаблоне равно pk_video=v.pk (VideoYouTubeRuTube.objects.get(pk=pk_video).pk)
def show_comments_and_form_comment_self_video(request, pk_video=None):
    # получаем одну запись видео, по параметру pk
    video_obj = VideoYouTubeRuTube.objects.get(pk=pk_video)

    # стандартная обработка формы
    if request.method == 'POST':
        form = CommentVideoYtRtForm(request.POST)
        if form.is_valid():
            # comment_for_self_video по сути одна запись комментария, назвать как угодно.
            # comment_for_self_video - название нигде не фигурирует, кроме этого метода
            comment_for_self_video = form.save(commit=False)  # commit=False, чтобы вписать автора и видео в модель комментария
            comment_for_self_video.author_comment = request.user  # вписываем автора в CommentVideoYtRt.author_comment
            comment_for_self_video.video = video_obj  # вписываем видео в CommentVideoYtRt.video
            comment_for_self_video.save()  # после проверки валидности сохраняем запись комментария
            # всплывающее окно при успешном создании коммента (отображу сверху страницы)
            messages.info(request, f'{request.user.username}! Комментарий к видео: "{video_obj.name}" - создан!')
            # при успешной отправке перенаправит на все видео, т.е останемся на той же странице
            return redirect('video_all')
    else:  # если ещё ничего не отправляли из формы
        form = CommentVideoYtRtForm()  # изначально просто пустая форма

    # получение всех комментариев к конкретному видео!
    all_comments_for_video = CommentVideoYtRt.objects.filter(video__pk=video_obj.pk)
    # то что необходимо передать в шаблон
    context = {
               'form': form,  # форма для отправки комментария
               'all_comments_for_video': all_comments_for_video,  # все комментарии к видео (модель комментарии к видео)
               'video_obj': video_obj,  # одна запись модели Видео
               'request': request,  # для того чтобы можно было сделать проверку аутентификации
               }
    # по дефолту в шаблон тега request не передаётся!
    return context  # передаём контекст, обрати внимание здесь без render, без request и без шаблона
