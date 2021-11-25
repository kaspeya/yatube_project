from django.http import HttpResponse

# Главная страница
def index(request):
    return HttpResponse('Главная страница')

#test

# Страница с постами, отфильтрованные по группам.
def group_posts(request,pk):
    return HttpResponse(f'Посты, отфильтрованные по группам {pk}')
