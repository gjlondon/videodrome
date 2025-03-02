from django.db import models

class User(models.Model):
    email = models.CharField(max_length=200, unique=True)

class Feed(models.Model):
    feed_uri = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=200)
    users = models.ManyToManyField(User)

class Post(models.Model):
    
    uri = models.CharField(max_length=1200, unique=True)
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=10002, blank=True)
    html = models.CharField(max_length=2000000, blank=True)
    random = models.CharField(max_length=10, default="random")

class Frame(models.Model):
    html = models.CharField(max_length=10000)
    post = models.ForeignKey(Post)
    seen = models.BooleanField(default=False)
