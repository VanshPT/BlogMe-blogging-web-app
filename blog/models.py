from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

def upload_to(instance, filename):
    return f"images/{filename}"
class Post(models.Model):
    pid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=15)
    content=models.TextField()
    slug=models.CharField(max_length=100)
    timestamp=models.DateTimeField(blank=True)
    image = models.ImageField(upload_to=upload_to, default='default-image.jpg')

    def __str__(self):
        return self.title+' - by '+self.author
    
class BlogComment(models.Model):
    cid=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp=models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[:13]+'... - '+self.user.username