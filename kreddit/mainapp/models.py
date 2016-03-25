import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils import timezone


class Subreddit(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.name

    @property
    def current_count(self):
        return self.post_set.all().count()

    @property
    def today_count(self):
        today = timezone.now() - datetime.timedelta(days=1)
        return self.post_set.filter(created_at__gte=today).count()

    @property
    def daily_average(self):
        week = timezone.now() - datetime.timedelta(days=7)
        return self.post_set.filter(created_at__gte=week).count() / 7



class Post(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=5000, validators=[MinLengthValidator(255)])
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)
    url = models.URLField()
    user = models.ForeignKey(User)
    subreddit = models.ForeignKey(Subreddit)

    def __str__(self):
        return self.title

    def is_recent(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.created_at

    def is_hot(self):
        # past 3 hours
        three_hours = timezone.now() - datetime.timedelta(hours=3)
        return self.comment_set.filter(created_at__gte=three_hours).count() > 3
# Post:
#
# id
# title
# description: needs to be longer than 255 characters
# url: which can be null and should use the built in urlfield type
# slug: This is a url friendly version of the title. SlugField
# creation time
# modification time
# Relationship to subreddit
# Relationship to a User
# method called is_recent
# -that returns True/False depending
# -on if the post is in the last day
# method called is_hot
# that returns True/False if the post
# has gotten more than 3 comments in the past 3 hours


class Comment(models.Model):
    description = models.CharField(max_length=5000, validators=[
                                                        MinLengthValidator(
                                                            255)])
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)

#  Comment:
#
# id
# comment text: needs to be longer than 255 characters
# relationship to User
# relationship to Post
# created time
# modified time