from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Count
from django.views.generic import ListView, DetailView, UpdateView, \
    CreateView

from mainapp.forms import SubredditForm, PostForm, CommentForm
from mainapp.models import Subreddit, Post, Comment


class SubredditList(ListView):

    model = Subreddit
    queryset = Subreddit.objects.annotate(num_posts=Count('post')) \
        .order_by('-num_posts')

    # paginate_by = 20
    # add if paginated to template


class SubredditDetail(DetailView):

    model = Subreddit
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.post_set.all().order_by('-created_at')
        return context


class PostDetail(DetailView):

    model = Post
    pk_url_kwarg = 'id'


class SubredditCreate(LoginRequiredMixin, CreateView):

    model = Subreddit
    form_class = SubredditForm

    success_url = reverse_lazy('subreddit_list')
    template_name_suffix = '_create'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SubredditUpdate(LoginRequiredMixin, UpdateView):

    model = Subreddit
    pk_url_kwarg = 'id'
    form_class = SubredditForm

    template_name_suffix = "_update"

    def get_success_url(self):
        return reverse('subreddit_detail', args=(self.object.id,))


class CommentDetail(DetailView):

    model = Comment
    pk_url_kwarg = 'id'


class PostCreate(LoginRequiredMixin, CreateView):

    model = Post
    form_class = PostForm
    pk_url_kwarg = 'id'

    template_name = 'mainapp/post_create.html'
    success_url = reverse_lazy('subreddit_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommentCreate(LoginRequiredMixin, CreateView):

    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'id'

    template_name = 'mainapp/comment_create.html'
    success_url = reverse_lazy('subreddit_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
