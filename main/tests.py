from django.test import TestCase
from models import User
import forgery_py
# Create your tests here.


class FollowFuncTestCase(TestCase):

    def setUp(self):
        self.u1 = User(
            email=forgery_py.internet.email_address(),
            username=forgery_py.internet.user_name(),
            password=forgery_py.lorem_ipsum.word())
        self.u1.save()
        self.u2 = User(
            email=forgery_py.internet.email_address(),
            username=forgery_py.internet.user_name(),
            password=forgery_py.lorem_ipsum.word())
        self.u2.save()

    def tearDown(self):
        self.u1.delete()
        self.u2.delete()

    def test_get_all(self):
        self.assertEqual(0, len(self.u1.follower.all()))
        self.assertEqual(0, len(self.u2.follower.all()))
        self.u1.follow(self.u2)
        self.assertEqual(1, len(self.u1.follower.all()))

    def test_is_following(self):
        self.assertFalse(self.u1.is_following(self.u2))

    def test_follow(self):
        self.u1.follow(self.u2)
        self.assertTrue(self.u1.is_following(self.u2))

    def test_is_followed_by(self):
        self.u1.follow(self.u2)
        self.assertTrue(self.u2.is_followed_by(self.u1))

    def test_unfollow(self):
        self.assertFalse(self.u1.is_following(self.u2))
        self.u1.follow(self.u2)
        self.assertTrue(self.u1.is_following(self.u2))
        self.assertTrue(self.u2.is_followed_by(self.u1))
        self.u1.unfollow(self.u2)
        self.assertFalse(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_followed_by(self.u1))
