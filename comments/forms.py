from django import forms
from comments.models import Comment


# форма для комментария
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # наша модель
        # поля отображаемые в форме
        fields = ['text_comment']
        widgets = {
            'text_comment': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }
