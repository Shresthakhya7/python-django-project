from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class Movie(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True)
    movie_name=models.CharField(max_length=100)
    movie_details=models.TextField()
    movie_image=models.ImageField(upload_to="media")