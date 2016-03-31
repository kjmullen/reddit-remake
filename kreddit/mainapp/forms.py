from mainapp.models import Subreddit, Post, Comment
from django import forms
from django.forms import Textarea


class SubredditForm(forms.ModelForm):
    """
    Form for making new subreddits
    name and description are only fields
    edit text area rows & cols for a bigger
    textarea
    """

    class Meta:

        model = Subreddit

        fields = ('name', 'description')
        widgets = {
            'description': Textarea(attrs={'rows':4, 'cols': 45})
        }


class PostForm(forms.ModelForm):
    """
    form for making new posts
    title, description, url, slug are fields
    subreddit has drop down to select which subreddit
    custom size of textarea for description at rows & cols
    """

    class Meta:

        model = Post

        fields = ('title', 'description', 'url', 'slug', 'subreddit')
        widgets = {
            'description': Textarea(attrs={'rows':4, 'cols': 45})
        }


class CommentForm(forms.ModelForm):
    """
    form for making new comments
    description is the only field
    post is a drop down menu to choose
    which post
    adjust textarea rows & cols  for
    custom sizing
    """

    class Meta:

        model = Comment

        fields = ('description', 'post')
        widgets = {
            'description': Textarea(attrs={'rows':4, 'cols': 45})
        }
