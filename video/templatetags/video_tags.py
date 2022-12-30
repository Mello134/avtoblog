from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from video.forms import CommentVideoYtRtForm
from video.models import VideoYouTubeRuTube, CommentVideoYtRt, LikeMarkVideo

# регистрируем этот файл в библиотеке
register = template.Library()

""" Здесь информация о конкретном видео внутри вложенного тега, одно видео это одна страничка видео, 
но показываем видео мы в списке, то есть есть представление всех видео, ListView,
вывод видео с помощью цикла for, и для каждой итерации есть свой собственный вложенный тег 
(комментарии для каждого видео, лайк закладка)"""


# тег получение формы комментария + самих комментариев для каждого видео (в списке видео)
@register.inclusion_tag('video/all_ralations_to_video.html')  # в скобках шаблон тега
# pk_video - (необходимо будет указывать в шаблоне, при вызове тега, думаю в цикле)
# pk_video в шаблоне равно pk_video=v.pk (VideoYouTubeRuTube.objects.get(pk=pk_video).pk)
def show_all_ralations_to_video(request, pk_video=None):
    # получаем одну запись видео, по параметру pk
    # video_obj = VideoYouTubeRuTube.objects.get(pk=pk_video)
    video_obj = VideoYouTubeRuTube.objects.get(pk=pk_video)
    # ЗДЕСЬ ОБРАБОТКА ФОРМЫ ДОБАВЛЕНИЯ КОММЕНТАРИЯ, НЕ СМОГ ОТДЕЛИТЬ ОТ ТЕГА, НО ВОЗМОЖНО ЭТО ВОЗМОЖНО
    # стандартная обработка формы
    if request.method == 'POST':
        form = CommentVideoYtRtForm(request.POST)
        if form.is_valid():
            # comment_for_self_video по сути одна запись комментария, назвать как угодно.
            # comment_for_self_video - название нигде не фигурирует, кроме этого метода
            comment_for_self_video = form.save(
                commit=False)  # commit=False, чтобы вписать автора и видео в модель комментария
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
        'total_likes_video': get_total_likes_video(video_obj),  # количество лайков на видео
        'likemarks_to_video': get_likemarks_to_video(request, pk_video),  # получение реакции лайк, закладка
        'form': form,  # форма для отправки комментария
        'all_comments_for_video': all_comments_for_video,  # все комментарии к видео (модель комментарии к видео)
        'video_obj': video_obj,  # одна запись модели Видео
        'request': request,  # для того чтобы можно было сделать проверку аутентификации
    }
    # по дефолту в шаблон тега request не передаётся!
    return context  # передаём контекст, обрати внимание здесь без render, без request и без шаблона


# Количество лайков на видео
def get_total_likes_video(video_obj):
    total_likes_video = LikeMarkVideo.objects.filter(video_lm__pk=video_obj.pk,
                                                     is_like_video=True).count()
    return total_likes_video


# Информация по реакции(лайк, закладка) пользователя на конкретное видео (нет или запись самой реакции)
def get_likemarks_to_video(request, pk_video):
    # пробуем получить реакцию пользователя на видео (была ли)
    likemarks_to_video = LikeMarkVideo.objects.filter(user_lm_video__pk=request.user.pk,
                                                      video_lm__pk=pk_video)
    if likemarks_to_video.count() > 0:  # если реакция уже была (от пользователя к видео)
        return likemarks_to_video  # возвращаем Queryset - запись из LikeMarkVideo
    else:  # реакции не было
        likemarks_to_video = 'no'  # меняем relation_video на 'no'
        return likemarks_to_video  # возвращаем no


# поведение кнопки лайк
@login_required
def like_video(request, pk_video):  # эти параметры будут браться из вложенного тега show_all_ralations_to_video
    video_obj = VideoYouTubeRuTube.objects.get(pk=pk_video)  # оцениваемое видео
    try:  # пробуем получить лайк и/или закладку авторизованного пользователя + на конкретное видео
        like_mark_video_object = LikeMarkVideo.objects.get(video_lm__pk=pk_video,
                                                           user_lm_video__pk=request.user.pk)
        # тоже самое что и like_mark_video_object.is_like_video == False:
        if not like_mark_video_object.is_like_video:  # если лай не стоит
            # ставим лайк
            LikeMarkVideo.objects.filter(video_lm__pk=pk_video,
                                         user_lm_video__pk=request.user.pk).update(is_like_video=True)
            messages.info(request, f"{request.user.username}! - вам понравилось видео: '{video_obj.name}'")
        else:  # если лайк стоит
            # убираем лайк
            LikeMarkVideo.objects.filter(video_lm__pk=pk_video,
                                         user_lm_video__pk=request.user.pk).update(is_like_video=False)
            messages.info(request, f"{request.user.username}! - вам больше не нравится видео: '{video_obj.name}'")
    except LikeMarkVideo.DoesNotExist:  # исключение (пользователь никогда не лайкал и не добавлял в закладки видео)
        # создаём новую реакцию
        like_mark_video_object = LikeMarkVideo.objects.create(
            user_lm_video=request.user,
            video_lm=video_obj,
            # video_obj = VideoYouTubeRuTube.objects.get(pk=pk_video)
            is_like_video=True,  # ставим лайк
            is_bookmarks_video=False  # закладку не создаём
        )
        like_mark_video_object.save()  # сохраняем запись в БД (LikeMarkVideo)
        messages.info(request, f"{request.user.username}! - вам понравилось видео: '{video_obj.name}'")
    return redirect('video_all')  # остаёмся на странице


# поведение кнопки закладки
@login_required
def bookmarks_video(request, pk_video):  # эти параметры будут браться из вложенного тега show_all_ralations_to_video
    video_obj = VideoYouTubeRuTube.objects.get(pk=pk_video)  # оцениваемое видео
    try:  # пробуем получить лайк и/или закладку авторизованного пользователя + на конкретное видео
        like_mark_video_object = LikeMarkVideo.objects.get(video_lm__pk=pk_video,
                                                           user_lm_video__pk=request.user.pk)
        # тоже самое что и like_mark_video_object.is_bookmarks_video == False:
        if not like_mark_video_object.is_bookmarks_video:  # если не в закладках
            # Добавляем в закладки
            LikeMarkVideo.objects.filter(video_lm__pk=pk_video,
                                         user_lm_video__pk=request.user.pk).update(is_bookmarks_video=True)
            messages.info(request, f"{request.user.username}! - Видео: '{video_obj.name}' - добавлено в ваши закладки")
        else:  # если уже в закладках
            # убираем из закладок
            LikeMarkVideo.objects.filter(video_lm__pk=pk_video,
                                         user_lm_video__pk=request.user.pk).update(is_bookmarks_video=False)
            messages.info(request, f"{request.user.username}! - Видео: '{video_obj.name}' - удалено из закладок")
    except LikeMarkVideo.DoesNotExist:  # исключение (пользователь никогда не лайкал и не добавлял в закладки видео)
        # создаём новую реакцию
        like_mark_video_object = LikeMarkVideo.objects.create(
            user_lm_video=request.user,
            video_lm=video_obj,
            # video_obj = VideoYouTubeRuTube.objects.get(pk=pk_video)
            is_like_video=False,  # Лайк не делаем
            is_bookmarks_video=True  # Добавляем в закладки
        )
        like_mark_video_object.save()  # сохраняем запись в БД (LikeMarkVideo)
        messages.info(request, f"{request.user.username}! - Видео: '{video_obj.name}' - добавлено в ваши закладки")
    return redirect('video_all')  # остаёмся на странице
