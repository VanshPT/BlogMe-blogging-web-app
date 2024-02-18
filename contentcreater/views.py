from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.models import User,Group
from blog.models import Post
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required



def content_creator_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Content-Creators').exists():
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'forbidden.html')
    return wrapper

@login_required
def homeCreater(request):
    is_content_creator = False
    if request.user.groups.filter(name='Content-Creators').exists():
        is_content_creator = True

    return render(request, 'index.html', {'is_content_creator': is_content_creator})


@login_required
@content_creator_required
def createBlog(request):
    is_content_creator = False
    if request.user.groups.filter(name='Content-Creators').exists():
        is_content_creator = True
        
    return render(request,'createBlog.html', {'is_content_creator': is_content_creator})

def signupCreater(request):
    if request.method == "POST":
        username=request.POST.get('username')
        firstname=request.POST.get('firstName')
        lastname=request.POST.get('lastName')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confpassword=request.POST.get('confirmPassword')
        if len(password)<8:
            messages.error(request,'Password Length Cannot be Less than 8!')
            return redirect('/create')
        elif password!=confpassword:
            messages.error(request,'Password and Confirm Password Fields do not Match!')
            return redirect('/create')
        elif len(password)<8 and password!=confpassword:
            messages.error(request,'Password Length Cannot be Less than 8!')
            messages.error(request,'Password and Confirm Password Fields do not Match!')
            return redirect('/create')
        elif not username.isalnum():
            messages.error(request, "Username should be in Alphabets or Numbers only!")
            return redirect('/create')
        else:
            # Create the user
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = firstname
            myuser.last_name = lastname
            myuser.save()

            # Assign the user to the 'Content-Creators' group
            reader_group, created = Group.objects.get_or_create(name='Content-Creators')
            myuser.groups.add(reader_group)

            # Display success message and redirect
            messages.success(request,'Congrats!! Your Blogme Creater Account has been successfully created')
            return redirect('/create')
    else:
        return HttpResponse("Error! Illegal Request")


def loginCreater(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user is not None:
            auth_login(request,user)
            messages.success(request, "Welome Creater!! Successfully Logged In!")
            return redirect('/create')
        else:
            messages.error(request, "Invalid Credentials! Please Try Again!")
            return redirect('/create')
    else:
        return HttpResponse("Error! Illegal Request")


def logoutCreater(request):
    auth_logout(request)  # Use renamed logout function
    messages.success(request, "Successfully Logged Out!")
    return redirect("/")