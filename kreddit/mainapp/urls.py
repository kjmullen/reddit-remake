from django.conf.urls import url

from mainapp.views import SubredditList, SubredditDetail, PostDetail, \
    SubredditCreate, SubredditUpdate, PostCreate, CommentCreate

urlpatterns = [
    url(r'^subreddits/$', SubredditList.as_view(), name="subreddit_list"),
    url(r'^subreddits/detail/(?P<id>\d+)/$', SubredditDetail.as_view(),
        name="subreddit_detail"),
    url(r'^posts/(?P<id>\d+)/$', PostDetail.as_view(), name="post_detail"),
    url(r'^subreddits/create/$', SubredditCreate.as_view(),
        name="subreddit_create"),
    url(r'^subreddits/update/(?P<id>\d+)/$', SubredditUpdate.as_view(),
        name="subreddit_update"),
    url(r'^subreddits/post_create/$', PostCreate.as_view(),
        name="post_create"),
    url(r'^subreddits/create_comment/$', CommentCreate.as_view(),
        name="comment_create"),
]
