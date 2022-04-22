from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


def paginator(request, post_list):
    paginator = Paginator(post_list, settings.PAGE_LIMIT)
    page_number = request.GET.get(settings.PAGE_NUMBER)
    page_obj = paginator.get_page(page_number)
    return page_obj


# Главная страница
def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    page_obj = paginator(request, post_list)
    context = {
        'post_list': post_list,
        'page_obj': page_obj,
    }
    return render(request, template, context)


# Страница с постами сообщества.
def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, template, context, slug)


# Страница профиля.
def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    post_list = author.posts.filter()
    page_obj = paginator(request, post_list)
    following = (request.user.is_authenticated
                 and author.following.filter(user=request.user).exists())
    context = {
        'page_obj': page_obj,
        'author': author,
        'following': following,
    }
    return render(request, template, context)


# Страница поста.
def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    comment_list = post.comments.all()
    page_obj = paginator(request, comment_list)
    context = {
        'post': post,
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, template, context)


# Страница создания поста.
@login_required
def post_create(request):
    template = 'posts/post_create.html'
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect('posts:profile', request.user)
    return render(request, template, {'form': form})


# Страница редактирования поста.
@login_required
def post_edit(request, post_id):
    template = 'posts/post_create.html'
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': is_edit,
    }
    return render(request, template, context)


# Страница создания комментария.
@login_required
def add_comment(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    author = request.user
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'post': post,
        'form': form,
        'author': author,
    }
    return render(request, template, context)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    post_list = Post.objects.filter(author__following__user=request.user).all()
    page_obj = paginator(request, post_list)
    context = {
        'post_list': post_list,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    if request.user.username == username:
        return redirect('posts:profile', request.user)
    following = get_object_or_404(User, username=username)
    Follow.objects.get_or_create(
        user=request.user,
        author=following,
    )
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    following = get_object_or_404(User, username=username)
    follower = get_object_or_404(Follow, author=following, user=request.user)
    follower.delete()
    return redirect('posts:profile', username)
