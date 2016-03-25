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
        """
        returns total number of posts in subreddit
        """
        return self.post_set.all().count()

    @property
    def today_count(self):
        """
        returns total number of posts within last 24 hours
        """
        today = timezone.now() - datetime.timedelta(days=1)

        return self.post_set.filter(created_at__gte=today).count()

    @property
    def daily_average(self):
        """
        returns average posts daily for last 7 days
        """
        week = timezone.now() - datetime.timedelta(days=7)

        return round(self.post_set.filter(created_at__gte=week).count() / 7, 2)

# Subreddit:
# *id
# *Name
# *Description
# *creation date time
# *method called current_count
# that returns how many posts
# *method called today_count
# that returns posts in the
# last 24 hours
# *method called daily_average
# that gets the average count
# of posts over the last 7 days


class Post(models.Model):

    title = models.CharField(max_length=300)

    description = models.CharField(max_length=5000, validators=[
                                                    MinLengthValidator(255)])

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    modified_at = models.DateTimeField(auto_now=True)

    url = models.URLField(null=True, blank=True)

    slug = models.SlugField(null=True, blank=True, max_length=100, unique=True)

    user = models.ForeignKey(User)

    subreddit = models.ForeignKey(Subreddit)

    def __str__(self):
        return self.title

    @property
    def is_recent(self):
        """
        returns true or false if post made within 24 hours
        """
        return timezone.now() - datetime.timedelta(days=1) <= self.created_at

    @property
    def is_hot(self):
        """
        true or false if comments > 3 within 3 hours
        """
        three_hours = timezone.now() - datetime.timedelta(hours=3)
        return self.comment_set.filter(created_at__gte=three_hours).count() > 3

# Post:
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

    user = models.ForeignKey(User)

    post = models.ForeignKey(Post)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    modified_at = models.DateTimeField(auto_now=True)

    description = models.CharField(max_length=5000, validators=[
                                                            MinLengthValidator(
                                                                        255)])

#  Comment:
# id
# comment text: needs to be longer than 255 characters
# relationship to User
# relationship to Post
# created time
# modified time
