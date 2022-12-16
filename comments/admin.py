from django.contrib import admin

from comments.models import Comment, LikeComment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'car_post', 'author_comment', 'text_comment')


admin.site.register(Comment, CommentAdmin)
admin.site.register(LikeComment)
