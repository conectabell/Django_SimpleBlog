from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import markdown


@login_required(login_url='django.contrib.auth.views.login')
def post_list(request):
    posts = Post.objects.filter(published_date__lte=
        timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required(login_url='django.contrib.auth.views.login')
def post_new(request):
    posts = Post.objects.filter(published_date__lte=
    timezone.now()).order_by('published_date')
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return post_list(request)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'posts': posts})


@login_required(login_url='django.contrib.auth.views.login')
def post_edit(request, pk):
    posts = Post.objects.filter(published_date__lte=
    timezone.now()).order_by('published_date')
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'posts': posts})


@login_required(login_url='django.contrib.auth.views.login')
def post_detail(request, pk):
    try:
        posts = Post.objects.filter(published_date__lte=
        timezone.now()).order_by('published_date')
        post = get_object_or_404(Post, pk=pk)
        #txt = markdown.markdown(post.text)
        #pst = {'author': post.author, 'title': post.title, 'text': txt,
                #'published_date': post.published_date,}
    except Exception as e:
        print e
    return render(request, 'blog/post_detail.html', {'post': post ,
                                                    'posts': posts})