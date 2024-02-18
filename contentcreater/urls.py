from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.homeCreater, name='homeCreater'),
    path('createBlog/', views.createBlog, name='createBlog'),
    path('signupCreater/', views.signupCreater, name='signupCreater'),
    path('loginCreater/', views.loginCreater, name='loginCreater'),
    path('logoutCreater/', views.logoutCreater, name='logoutCreater'),
]
