from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from comments.models import Comment, LikeComment


# поведение кнопки лайк
@login_required
def like_button_comment(request, cat_slug, car_slug, com_id):
    # или 404 или Comment.objects.get(pk=com_id)
    # comment - жто поле модели LikeComment-> ForeignKey -> Comment
    comment = get_object_or_404(Comment, pk=com_id)
    # author_comment = comment.author_comment  # только для вывода во всплывающем сообщении

    # получаем или создаём запись в модели LikeComment (то есть лайк)
    like_comment, created = LikeComment.objects.get_or_create(
        comment=comment,
        user=request.user
    )

    # если запись не создалась (т.е она уже была)
    if not created:
        like_comment.delete()
        # messages.info(request, f"Вам больше не нравится комментарий от пользователя - {author_comment}")
    else:  # если запись добавилась - (лайкнули)
        like_comment.save()  # сохраняем лайк (запись LikeComment) в БД
        # messages.info(request, f'Вам понравился комментарий от пользователя - {author_comment}')
    # остаёмся на странице поста, через запятую все динамические параметры (получали с request)
    return redirect('car', cat_slug, car_slug)


# кнопка удаления комментария
def delete_button_comment(request, cat_slug, car_slug, com_id):
    # получаю 1 комментарий (по id коммента)
    comment = get_object_or_404(Comment, pk=com_id)
    # если пользователь автор коммента или админ (id 1)
    if request.user.id == comment.author_comment.id or request.user.id == 1:
        # Удаляем комментарий
        comment.delete()
    else:  # если не автор и не админ
        # Вывожу сообщение
        messages.warning(request, 'Вы не можете удалить не свой комментарий')
    # перенаправляюсь на страницу поста
    # обязательно указать динамические параметры
    return redirect('car', cat_slug, car_slug)
