from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils import timezone
# Create your models here.

class StudentName(models.Model):
    name = models.CharField(max_length=30)
    fname = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    entry = models.CharField(max_length=20)
    image = models.ImageField(upload_to = "images/")
    present = models.BooleanField(default=False)
    updated = models.DateTimeField(null=True)
    def __str__(self):
        return self.name


