from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2, 
                'placeholder': 'Ваш комментарий...', 
                'class': 'form-control textarea'
                })
            
        }
