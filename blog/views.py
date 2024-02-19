from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras
from itertools import chain

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    latest_post = allPosts.order_by('-timestamp').first()
    context = {'allPosts': allPosts, 'latest_post': latest_post}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    totalcomments = list(chain(comments, replies))
    replyDict = {}

    for reply in replies:
        if reply.parent.cid not in replyDict:
            replyDict[reply.parent.cid] = [reply]
        else:
            replyDict[reply.parent.cid].append(reply)
    
    context = {
        'post': post,
        'comments': comments,
        'user': request.user,
        'replyDict': replyDict,
        'totalcomments': totalcomments
    }
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postId = request.POST.get('postId')
        post = Post.objects.filter(pid=postId).first()
        commentId = request.POST.get('parentId')

        if commentId == None:
            comment = BlogComment(comment=comment, user=user, post=post)
            messages.success(request, "Comment added successfully!")
        else:
            parent = BlogComment.objects.filter(cid=commentId).first()
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            messages.success(request, "Reply added successfully!")
        
        comment.save()
    return redirect(f'/blog/{post.slug}')
