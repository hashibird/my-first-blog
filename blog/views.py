from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm
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

@login_required
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

@login_required
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

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(Q(published_date__isnull=True) | Q(published_date__gte=timezone.now())).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published_date = timezone.datetime.now() + timezone.timedelta(weeks=100)
    post.save()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        Comment.name = 'anonymous'
        Comment.text = ''
        form = CommentForm(instance=Comment)
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approved_comment = False
    comment.save()
    return redirect('post_detail', pk=comment.post.pk)


