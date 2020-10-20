from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm, CategoryForm
from .models import Follow, Group, Post, User, Category


def index(request):
    post_list = Post.objects.select_related('author')
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator
    }
    return render(request, 'index.html', context)


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index', permanent=True)

    context = {
        'form': form,
    }
    return render(request, 'new_post.html', context)


@login_required
def new_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('index', permanent=True)
    
    context = {
        'form': form,
    }
    return render(request, 'new_category.html', context)


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    post_list = category.posts.all()
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'group': category,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'category.html', context)


def group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    subgroup_list = group.category.all()
    paginator = Paginator(subgroup_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'group': group,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'group.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = Follow.objects.filter(
        user__username=request.user,
        author=author
    ).exists()

    context = {
        'page': page,
        'paginator': paginator,
        'author': author,
        'following': following
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    items = post.comments.all()
    author = post.author
    form = CommentForm(request.POST or None, files=request.FILES or None)

    context = {
        'post': post,
        'author': author,
        'items': items,
        'form': form
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    author = post.author
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)

    if request.user != author:
        return redirect('post', username=username, post_id=post_id, permanent=True)

    if form.is_valid():
        form.save()
        return redirect('post', username=username, post_id=post_id, permanent=True)

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'new_post.html', context)


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    form = CommentForm(request.POST or None, files=request.FILES or None)
    items = post.comments.all()

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('post', username=username, post_id=post_id, permanent=True)

    context = {
        'form': form,
        'post': post,
        'items': items
    }
    return render(request, 'post.html', context)


@login_required
def profile_follow(request, username):
    follower = get_object_or_404(User, username=request.user)
    author = get_object_or_404(User, username=username)
    if author != follower:
        Follow.objects.get_or_create(user=follower, author=author)
    return redirect('follow_index')


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator
    }
    return render(request, 'follow.html', context)


@login_required
def profile_unfollow(request, username):
    follower = get_object_or_404(User, username=request.user)
    author = get_object_or_404(User, username=username)
    if author != follower:
        follow = Follow.objects.get(user=follower, author=author)
        follow.delete()
    return redirect('follow_index')
