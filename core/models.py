from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime, uuid


class User(AbstractUser):
    is_worker = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    username = models.CharField(max_length=200, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=500, blank=True, null=True, unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to='images/', default="profiles/user-default.png")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    username = models.CharField(max_length=200, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=500, blank=True, null=True, unique=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to='profiles/', default="profiles/user-default.png")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url


class Schedule(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now_add=False, default=datetime.time(hour=8, minute=0))
    end_time = models.TimeField(auto_now_add=False, default=datetime.time(hour=17, minute=0))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.worker) + " " + str(self.start_time) + " " + str(self.end_time)
