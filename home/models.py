from django.db import models

# Create your models here.
class Contact(models.Model):
    cid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.name