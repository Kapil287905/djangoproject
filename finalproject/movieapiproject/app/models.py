from django.db import models

# Create your models here.
class Movie(models.Model):
    title=models.CharField(max_length=30)
    rating=models.PositiveIntegerField()
    duration=models.CharField(max_length=40)
    type=(('sci-fi','sci-if'),('social','social'),('bio','bio'))
    category=models.CharField(max_length=50,choices=type)
    photo=models.URLField()