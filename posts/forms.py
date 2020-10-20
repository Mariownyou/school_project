from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Comment, Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'text', 'is_important', 'image')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('group', 'title', 'slug')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
