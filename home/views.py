from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User,Group
from blog.models import Post
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
def home(request):
    allPosts = Post.objects.all().order_by('-timestamp')[:8]
    return render(request, 'home/home.html', {'allPosts': allPosts})


def contact(request):

    if request.method=='POST':
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        message=request.POST.get('message','')
        if len(name)<2 or len(email)<3 or len(phone)< 10 or len(message)<4:
            messages.error(request, "Please fill the form correctly!")

        contact=Contact(name=name, email=email, phone=phone, content=message)
        contact.save()
        messages.success(request, "Your message is sent successfully")
        
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    query=request.GET.get('search')
    if len(query)>100:
        allPosts=[]
    else:
        allPostsTitle=Post.objects.filter(title__icontains=query)
        allPostsContent=Post.objects.filter(content__icontains=query)
        allPostsAuthor=Post.objects.filter(author__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent,allPostsAuthor)
    if allPosts.count() == 0:
        messages.error(request,"Please Fill the form correctly!")
    context={'allPosts':allPosts, 'query':query}
    return render(request, 'home/search.html', context)

def signup(request):
    if request.method == "POST":
        username=request.POST.get('username')
        firstname=request.POST.get('firstName')
        lastname=request.POST.get('lastName')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confpassword=request.POST.get('confirmPassword')
        if len(password)<8:
            messages.error(request,'Password Length Cannot be Less than 8!')
            return redirect('/')
        elif password!=confpassword:
            messages.error(request,'Password and Confirm Password Fields do not Match!')
            return redirect('/')
        elif len(password)<8 and password!=confpassword:
            messages.error(request,'Password Length Cannot be Less than 8!')
            messages.error(request,'Password and Confirm Password Fields do not Match!')
            return redirect('/')
        elif not username.isalnum():
            messages.error(request, "Username should be in Alphabets or Numbers only!")
            return redirect('/')
        else:
            # Create the user
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = firstname
            myuser.last_name = lastname
            myuser.save()

            # Assign the user to the 'Reader' group
            reader_group, created = Group.objects.get_or_create(name='Reader')
            myuser.groups.add(reader_group)

            # Display success message and redirect
            messages.success(request,'Your Blogme Account has been successfully created')
            return redirect('/')
    else:
        return HttpResponse("Error! Illegal Request")


def login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user is not None:
            auth_login(request,user)
            messages.success(request, "Successfully Logged In!")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials! Please Try Again!")
            return redirect('/')
    else:
        return HttpResponse("Error! Illegal Request")


def logout(request):
    auth_logout(request)  # Use renamed logout function
    messages.success(request, "Successfully Logged Out!")
    return redirect("/")