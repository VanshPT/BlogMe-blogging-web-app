from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post

# Create your views here.
def blogHome(request):
    allPosts=Post.objects.all()
    latest_post = allPosts.order_by('-timestamp').first()
    context={'allPosts':allPosts, 'latest_post':latest_post}
    return render(request, 'blog/blogHome.html' , context)

def blogPost(request,slug):
    post=Post.objects.filter(slug=slug).first()
    print(post)
    context={'post':post}
    return render(request, 'blog/blogPost.html' , context)