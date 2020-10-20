from django import forms

from .models import Comment, Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'text', 'image')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('group', 'slug', 'title')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
