from django import forms
from trumbowyg.widgets import TrumbowygWidget


from .models import Comment, Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'text', 'is_important', 'image', 'video')
        widgets = {
            'text': TrumbowygWidget(),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('group', 'title', 'slug')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
