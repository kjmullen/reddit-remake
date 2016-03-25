from django.contrib import admin
from mainapp.models import Subreddit, Post, Comment


@admin.register(Subreddit)
class SubredditAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'current_count', 'today_count', 'daily_average')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'url', 'is_hot', 'created_at', 'modified_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'description', 'user', 'created_at', 'modified_at')