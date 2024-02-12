from django.urls import path,include
from . import views

urlpatterns = [

    # apis here
    path('postComment/', views.postComment, name='postComment'),

    path('', views.blogHome, name='blogHome'),
    path('<str:slug>/', views.blogPost, name='blogPost'),
    

]
