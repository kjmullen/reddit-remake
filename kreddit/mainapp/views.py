from django.core.urlresolvers import reverse
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from mainapp.forms import SubredditForm
from mainapp.models import Subreddit, Post


class SubredditList(View):

    def get(self, request):

        subreddits = Subreddit.objects.annotate(num_posts=Count('post'))\
            .order_by('-num_posts')

        return render(request, "mainapp/subreddit_list.html",
                      {"subreddits": subreddits})


class SubredditDetail(View):

    def get(self, request, id):

        subreddit = get_object_or_404(Subreddit, pk=id)
        posts = subreddit.post_set.order_by('-created_at')[:20]

        return render(request, "mainapp/subreddit_detail.html",
                      {"subreddit": subreddit, "posts": posts})


class PostDetail(View):

    def get(self, request, id):

        post = get_object_or_404(Post, pk=id)
        comments = post.comment_set.order_by('-created_at')

        return render(request, "mainapp/post_detail.html",
                      {'post': post, 'comments': comments})


class SubredditCreate(View):

    def get(self, request):
        form = SubredditForm()

        return render(request, "mainapp/subreddit_create.html",
                      {"form": form})

    def post(self, request):

        form = SubredditForm(request.POST)

        if form.is_valid():
            subreddit = form.save(commit=False)
            subreddit.user = request.user
            subreddit.save()

            return redirect(reverse("subreddit_list"))

        return render(request, "mainapp/subreddit_create.html",
                      {"form": form})


class SubredditUpdate(View):

    def get(self, request, id):

        subreddit = get_object_or_404(Subreddit, pk=id)
        form = SubredditForm(instance=subreddit)

        return render(request, "mainapp/subreddit_update.html",
                      {"form": form, "subreddit": subreddit})

    def post(self, request, id):
        subreddit = get_object_or_404(Subreddit, pk=id)

        form = SubredditForm(data=request.POST, instance=subreddit)

        if form.is_valid():
            subreddit = form.save(commit=False)
            subreddit.user = request.user
            subreddit.save()

            return redirect(reverse("subreddit_list"))
        return render(request, "mainapp/subreddit_update.html",
                      {"form": form, "subreddit": subreddit})
