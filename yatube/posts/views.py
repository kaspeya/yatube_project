from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.conf import settings

# Главная страница
def index(request):
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    # Сортировка постов по полю pub_date по убыванию.
    posts = Post.objects.all()[:settings.PAGE_LIMIT]
    context = {
        'title': title,
        'posts': posts,
    }
    return render(request, template, context)

# Страница с постами сообщества.
def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
     # Сортировка постов по полю pub_date по убыванию.
    posts = group.posts.all()[:settings.PAGE_LIMIT]
    group_list_title = 'Записи сообщества ' + group.title
    context = {
        'group': group,
        'posts': posts,
        'title':group_list_title,
    }
    return render(request, template, context, slug)
