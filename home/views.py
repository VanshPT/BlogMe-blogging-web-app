from django.shortcuts import render
from .models import Contact
from django.contrib import messages
# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

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