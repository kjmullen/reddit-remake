import datetime
from django.test import TestCase
from mainapp.models import Subreddit, Post, PostVote, Comment, CommentVote
from django.contrib.auth.models import User
from django.utils import timezone


class KredditTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user\
                                            (
                                            username="SubredditTest",
                                            email="subreddit@test.com",
                                            password="password"
                                                                            )

        self.testsubreddit = Subreddit.objects.create\
                                            (
                                            description="Testing my Subreddit",
                                            name="TestSubReddit"
                                                                            )

        self.testpost = Post.objects.create(
                                            title="PostTest",
                                            description="This is a test post.",
                                            url="test.com",
                                            slug="postslug",
                                            user=self.user,
                                            subreddit=self.testsubreddit
                                                                            )

    def test_today_count(self):
        self.testsubreddit.post_set.create\
                                            (
                                            title="PostTest2",
                                            description="Test post 2",
                                            url="2ndtest.com",
                                            slug="2ndpostslug",
                                            user=self.user,
                                            subreddit=self.testsubreddit
                                                                            )
        self.assertEqual(self.testsubreddit.current_count,
                                            2, "Post count broken."
                                                                            )



