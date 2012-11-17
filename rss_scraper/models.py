from django.db import models

class User(models.Model):
    email = models.CharField(max_length=200)

class Feed(models.Model):
    feed_uri = models.CharField(max_length=200)
    users = models.ManyToManyField(User)

class Post(models.Model):
    uri = models.CharField(max_length=1200)
    post = models.ForeignKey(Feed)
    html = models.CharField(max_length=20000)

class Frame(models.Model):
    html = models.CharField(max_length=10000)
    post = models.ForeignKey(Post)
