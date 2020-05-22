from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import BlogPost
def index(request):
    all_Post = []
    allPosts = BlogPost.objects.all()
    for i in allPosts:
        all_Post.append(i)
    param = {'all_Post': all_Post}
    return  render(request,'blog/index.html',param)

def blogPost(request,id):
    prev_id = id - 1
    next_id = id + 1
    try:
        prev = BlogPost.objects.filter(post_id=prev_id)[0]
    except:
        prev = ""
    try:
        next = BlogPost.objects.filter(post_id=next_id)[0]
    except:
        next = ""

    post = BlogPost.objects.filter(post_id=id)[0]
    return render(request, 'blog/blogPost.html',{'post':post,'prev':prev,'next':next})