from django.contrib import admin
from mainapp.models import Subreddit, Post, Comment, PostVote, CommentVote


@admin.register(Subreddit)
class SubredditAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'current_count',
                    'today_count', 'daily_average')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'link_karma', 'up_votes', 'subreddit', 'title', 'description', 'url', 'slug', 'is_hot',
                    'is_recent', 'created_at', 'modified_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'up_votes', 'comment_karma', 'post', 'description', 'user', 'created_at',
                    'modified_at')


@admin.register(PostVote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('why', 'post', 'created_at')


@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    list_display = ('why', 'comment', 'created_at')