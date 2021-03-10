from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
import datetime
# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    today = datetime.date.today()
    return render(request, 'blog/post_list.html', {'posts': posts, 'today': today})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    timenow = timezone.now()
    return render(request,'blog/post_detail.html', {'post': post, 'timenow': timenow})