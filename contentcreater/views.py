from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.models import User,Group
from blog.models import Post
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template.defaultfilters import slugify
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def content_creator_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Content-Creators').exists():
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'forbidden.html')
    return wrapper

def homeCreater(request):
    is_content_creator = request.user.groups.filter(name='Content-Creators').exists()
    return render(request, 'index.html', {'is_content_creator': is_content_creator})

@login_required
@content_creator_required
def createBlog(request):
    is_content_creator = request.user.groups.filter(name='Content-Creators').exists()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        blog_content = request.POST.get('blog_content')
        image = request.FILES.get('image')  # Get the uploaded image file
        
        if title and blog_content:
            slug = slugify(title)
            post = Post(title=title, author=author, content=blog_content, slug=slug, timestamp=timezone.now())

            if image:  # Check if an image is uploaded
                # Resize and save the image
                resized_image = resize_image(image)
                post.image = resized_image

            post.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('/create/createBlog/')
        else:
            messages.error(request, 'Title and content are required!')
    
    return render(request, 'createBlog.html', {'is_content_creator': is_content_creator})

def resize_image(image):
    # Open the uploaded image
    img = Image.open(image)

    # Convert image to RGB mode if it's in paletted mode (P mode)
    if img.mode == 'P':
        img = img.convert('RGB')

    # Define the desired width and height for the resized image
    desired_width = 1600  # Twice the width of 800
    desired_height = 800  # Twice the height of 400

    # Resize the image while preserving aspect ratio
    img.thumbnail((desired_width, desired_height))

    # Convert the image to BytesIO object
    output_io = BytesIO()
    img.save(output_io, format='JPEG')
    output_io.seek(0)

    # Create a new InMemoryUploadedFile instance for the resized image
    resized_image = InMemoryUploadedFile(output_io, None, image.name, 'image/jpeg', output_io.getbuffer().nbytes, None)

    return resized_image



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