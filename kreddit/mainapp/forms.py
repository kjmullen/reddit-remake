from mainapp.models import Subreddit, Post, Comment
from django import forms
from django.forms import Textarea


class SubredditForm(forms.ModelForm):

    class Meta:

        model = Subreddit

        fields = ('name', 'description')
        widgets = {
            'description': Textarea(attrs={'rows':4, 'cols': 45})
        }


class PostForm(forms.ModelForm):

    class Meta:

        model = Post

        fields = ('title', 'description', 'url', 'slug', 'subreddit')
        widgets = {
            'description': Textarea(attrs={'rows':4, 'cols': 45})
        }


class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment

        fields = ('description', 'post')
        widgets = {
            'description': Textarea(attrs={'rows':4, 'cols': 45})
        }
