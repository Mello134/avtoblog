from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404

from video.forms import CommentVideoYtRtForm
from video.models import VideoYouTubeRuTube, CommentVideoYtRt, LikeMarkVideo, LikeCommentVideoYtRt

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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # остаёмся на странице предыдущей!
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
    # 1 - мы находимся например на странице - http://127.0.0.1:8000/video/bookmarks/
    # 2 - при нажатии лайка, наш путь будет примерно - http://127.0.0.1:8000/video/like_video/9/
    # 3 - нам нужно вернуться на первый путь - http://127.0.0.1:8000/video/bookmarks/
    # 3 - для этого - return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # остаёмся на странице предыдущей!


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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # остаёмся на странице предыдущей!


# вложенный тег получение (отображения) блока лайка на отдельный комментарий к видео
@register.inclusion_tag('video/like_to_comment_video.html')  # в скобках шаблон тега
# pk_com - (необходимо будет указывать в шаблоне, при вызове тега в цикле перебора комментариев)
# pk_video в шаблоне равно pk_video=v.pk (VideoYouTubeRuTube.objects.get(pk=pk_video).pk)
def show_like_to_comment_video(request, pk_com=None):

    # получаем количество лайков для конкретного поста.
    like_comment_count = LikeCommentVideoYtRt.objects.filter(comment__pk=pk_com).count()

    # Получаем объект лайка (конкретный пользователь/конкретный комментарий)
    like_obj = LikeCommentVideoYtRt.objects.filter(user__pk=request.user.pk,
                                                   comment__pk=pk_com)

    # получаем информацию лайкнул ли авторизованный пользователь конкретный комментарий
    if like_obj.count() > 0:  # если нашли запись в модели LikeCommentVideoYtRt (лайк есть)
        is_liked_comment = True  # Лайкал
    else:  # ели записи нет (то есть пользователь не лайкал этот коммент)
        is_liked_comment = False  # НЕ лайкал

    # запишу в словарь все параметры которые нужно передать в шаблон тега
    context = {
        'request': request,  # для того чтобы можно было сделать проверку аутентификации
        'is_liked_comment': is_liked_comment,  # лайкнул ли пользователь коммент
        'like_comment_count': like_comment_count,  # количество лайков на комменте от всех пользователей
        'pk_com': pk_com,  # id комментария
    }
    # передаю словарь в шаблоне тега
    return context


# логика кнопки лайк для комментария
@login_required
def like_button_comment_video(request, pk_com):
    # пробую получить запись комментария
    comment = get_object_or_404(CommentVideoYtRt, pk=pk_com)

    # LikeCommentVideoYtRt
    # получаю или создаю запись лайка к комментарию, если её нет создаю
    like_comment_video, created = LikeCommentVideoYtRt.objects.get_or_create(
        comment=comment,
        user=request.user
    )

    # проверка создался ли комментарий
    if not created:  # Если запись не создалась (т.е. она уже была)
        like_comment_video.delete()  # удаляем запись = удаляем лайк
        messages.info(request, f"Вам больше не нравиться комментарий, пользователя: {comment.author_comment}.")
    else:  # если запись создалась (т.е поставили лайк)
        like_comment_video.save()  # сохраняем в БД запись лайка
        messages.info(request, f"Вам понравился комментарий, пользователя: {comment.author_comment}.")

    # перенаправляемся/остаёмся на странице списка видео
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # остаёмся на странице предыдущей!


# логика кнопки удаления комментария
@login_required
def delete_comment_video_button(request, pk_com):
    # пробую получить запись комментария
    comment = get_object_or_404(CommentVideoYtRt, pk=pk_com)

    # если вы автор комментария или админ
    if comment.author_comment.pk == request.user.pk or request.user.pk == 1:
        comment.delete()  # удаляю запись комментарий
        messages.info(request, f"{request.user.username} - удалил комментарий!")
    else:
        messages.info(request, f"{request.user.username} - вы не можете удалить чужой комментарий!")

    # перенаправляемся/остаёмся на странице списка видео
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # остаёмся на странице предыдущей!
