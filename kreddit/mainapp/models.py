import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db.models import Q
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

    description = models.CharField(max_length=5000,
                                   validators=[MinLengthValidator(255)])

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

    def up_votes(self):

        return self.postvote_set.filter(why__contains='U').count() - \
               self.postvote_set.filter(why__contains='D').count()

    up_votes.short_description = "Vote Score"

    def link_karma(self):
        if self.url:
            return self.postvote_set.filter(Q(why__contains="U") |
                                            Q(why__contains="D")).count()


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

    def up_votes(self):
        return self.commentvote_set.filter(
            why__contains='U').count() - self.commentvote_set.filter(
            why__contains='D').count()
    up_votes.short_description = "Vote Score"

    def comment_karma(self):
        return self.commentvote_set.filter(Q(why__contains="U") |
                                           Q(why__contains="D")).count()

    def __str__(self):
        return self.description[:30]

#  Comment:
# id
# comment text: needs to be longer than 255 characters
# relationship to User
# relationship to Post
# created time
# modified time


class PostVote(models.Model):

    UP = 'U'
    DOWN = 'D'

    votes = (
        (UP, 'Upvote'),
        (DOWN, 'Downvote'),
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    why = models.CharField(max_length=8, choices=votes, null=True, blank=True)


class CommentVote(models.Model):

    UP = 'U'
    DOWN = 'D'

    votes = (
        (UP, 'Upvote'),
        (DOWN, 'Downvote'),
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
    why = models.CharField(max_length=8, choices=votes, null=True, blank=True)

# Hard Mode
# Implement the voting system.
# Both comments and posts can
# be voted up and down it is
# your choice how this is
# implemented in the system.
# One note is that you probably
# want to store the up and down
# votes individually with timestamps
#
# Comments and Posts should have
# methods that allow for them to
# calculate the total value of
# up-votes - down-votes.
#
# Implement karma. Reddit has
# 2 karma indicators link karma
# and comment karma. For this
# project both karma are calculated
# as the sum of each item’s total
# (from previous objective).
#
# Implement the ManyToMany
# Relationship with Trophies
#
# Posts can be sorted in a few
# ways in reddit. Implement
# the following as described.
# You will need to do these in
# the django shell and add a
# python file with the code as
# part of your project.
#
# -New: Chronologically newest to oldest
    # Post.objects.all().order_by("-created_at")
# -Top: Highest rated for the last 24 hours
    # Post.objects.filter(created_at__gte=today).order_by("-rating")
# -Hot: Ordered by amount of up-votes in the 3 hours
    # Post.objects.filter(created_at__gte=three_hours)
    # .order_by("-rating in last 3 hours")

# -Controversial: Ordered by posts with a high number
#  of both up and down votes
#
# -The User object is part of the core auth library.
#  There are a few ways to extend its functionality.
#  Historically, the way it works is that you create
#  a profile object with a OneToOne relationship to User.
#  Implement this object then create
#  methods on it to retrieve:
#
# Link karma for the user
#
# Comment karma for the user
#
# Average up-votes
#
# Average down-votes
#
# Total counts for comments and links