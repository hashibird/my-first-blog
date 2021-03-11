from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Post
from .forms import PostForm
import datetime
# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    today = datetime.date.today()
    return render(request, 'blog/post_list.html', {'posts': posts, 'today': today})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    timenow = timezone.now()
    return render(request,'blog/post_detail.html', {'post': post, 'timenow': timenow})

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        new = 'new'
        form = PostForm(initial={'published_date': timezone.now()})
    return render(request, 'blog/post_edit.html', {'form': form, 'new': new})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        if post.published_date:
            form = PostForm(instance=post)
        else:
            post.published_date = timezone.now()
            form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Post.objects.filter(Q(published_date__isnull=True) | Q(published_date__gte=timezone.now())).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')