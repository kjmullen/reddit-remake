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