from django.db import models

# Create your models here.
class Post(models.Model):
    pid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=15)
    content=models.TextField()
    slug=models.CharField(max_length=100)
    timestamp=models.DateTimeField(blank=True)

    def __str__(self):
        return self.title+' - by '+self.author