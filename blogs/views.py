from .forms import BlogPostForm
from django.shortcuts import render
from .forms import UserRegisterForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.user == post.author or request.user.is_staff:
        post.delete()
        # Перенаправление на страницу со всеми постами после удаления
        return redirect('index')
    else:
        # Добавьте обработку ошибки или перенаправление, если пользователь не имеет прав на удаление
        return redirect('index')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Добавьте логику входа в систему или перенаправления здесь
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def new_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)  # Сохраняем форму, но пока не коммитим в базу данных
            new_post.author = request.user  # Устанавливаем автора поста в текущего пользователя
            new_post.save()  # Теперь сохраняем пост в базу данных
            return redirect('index')
    else:
        form = BlogPostForm()
    return render(request, 'blogs/new_post.html', {'form': form})

def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method != 'POST':
        form = BlogPostForm(instance=post)
    else:
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)

def index(request):
    posts = BlogPost.objects.order_by('-date_added')
    context = {'posts': posts}
    return render(request, 'blogs/index.html', context)
