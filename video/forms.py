from django import forms
from video.models import CommentVideoYtRt, VideoYouTubeRuTube


# форма создания нового видеопоста
class VideoYouTubeRuTubeForm(forms.ModelForm):
    class Meta:
        model = VideoYouTubeRuTube
        fields = ['name', 'video_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control, col-6'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control, col-6'}),
        }


# форма редактирования видеопоста
class VideoYouTubeRuTubeUpdateForm(forms.ModelForm):
    class Meta:
        model = VideoYouTubeRuTube
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control, col-6'})}


# форма создания комментария к видео
class CommentVideoYtRtForm(forms.ModelForm):
    class Meta:
        model = CommentVideoYtRt
        # поля отображаемые в форме
        fields = ['text_comment']
        # widgets = атрибуты в html, rows = строк в форме, form-control = bootstrap5 class
        widgets = {
            'text_comment': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }
