from mainapp.models import Subreddit
from django import forms
from django.forms import Textarea


class SubredditForm(forms.ModelForm):

    class Meta:

        model = Subreddit

        fields = ('name', 'description')
        widgets = {
            'description': Textarea(attrs={'rows':4, 'cols': 45})
        }
