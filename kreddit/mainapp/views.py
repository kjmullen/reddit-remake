from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Count
from django.views.generic import ListView, DetailView, UpdateView, \
    CreateView

from mainapp.forms import SubredditForm, PostForm, CommentForm
from mainapp.models import Subreddit, Post, Comment


class SubredditList(ListView):
    """
    uses subreddit model
    ordered by number of posts in subreddits
    10 subreddits allowed per page @ paginate_by
    """

    model = Subreddit
    queryset = Subreddit.objects.annotate(num_posts=Count('post')) \
        .order_by('-num_posts')
    paginate_by = 10


class SubredditDetail(DetailView):
    """
    gets the post of the subreddit selected
    ordered by when they were created
    newest to oldest
    """

    model = Subreddit
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.post_set.all().order_by('-created_at')
        return context


class PostDetail(DetailView):
    """
    sets post model to display details
    by id
    """

    model = Post
    pk_url_kwarg = 'id'


class SubredditCreate(LoginRequiredMixin, CreateView):
    """
    create a new subreddit
    uses subreddit model & SubredditForm form_class
    when subreddit is created, it returns user to
    subreddit list
    """
    model = Subreddit
    form_class = SubredditForm

    success_url = reverse_lazy('subreddit_list')
    template_name_suffix = '_create'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SubredditUpdate(LoginRequiredMixin, UpdateView):
    """
    option to update subreddit's name+description
    uses SubredditForm for form_class
    successful update form will return user to the details
    of that subreddit by id
    """

    model = Subreddit
    pk_url_kwarg = 'id'
    form_class = SubredditForm

    template_name = "mainapp/subreddit_update.html"

    def get_success_url(self):
        return reverse('subreddit_detail', args=(self.object.id,))


class CommentDetail(DetailView):
    """
    gets comment model for details
    by id
    """

    model = Comment
    pk_url_kwarg = 'id'


class PostCreate(LoginRequiredMixin, CreateView):
    """
    uses Post model and PostForm form_class.
    returns user to subreddit list after successful
    post.
    """

    model = Post
    form_class = PostForm
    pk_url_kwarg = 'id'

    template_name = 'mainapp/post_create.html'
    success_url = reverse_lazy('subreddit_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommentCreate(LoginRequiredMixin, CreateView):
    """
    used to create comments
    uses comment model + CommentForm form_class
    """
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'id'

    template_name = 'mainapp/comment_create.html'
    success_url = reverse_lazy('subreddit_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
