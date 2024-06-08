from django.contrib.auth.models import User
from django.test import TestCase
from taggit.models import Tag

from blog.models import Profile, Post


def create_default_user():
    user = User(
        username='testuser',
        email='test@gmail.com',
    )
    user.set_password("rohlik123")
    user.save()

    profile = Profile(user=user)
    profile.save()

    return user


# Create your tests here.
class TestUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_default_user()

    def test_user_with_profile_exists(self):
        user = User.objects.get(id=1)

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertNotEqual(user.password, 'rohlik123')
        self.assertEqual(user.id, 1)
        self.assertEqual(user.profile.id, 1)


class TestPostModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = create_default_user()

        post = Post(
            title="Learning Python",
            slug="learning-python",
            body="django, fastapi",
            status=Post.Status.PUBLISHED,
            author=user,
        )
        post.save()

        # user = User(
        #     username='testuser',
        #     email='test@gmail.com',
        #     password='rohlik123',
        # )
        # user.save()
        #
        # profile = Profile(user=user)
        # profile.save()

    def test_post(self):
        post = Post.objects.get(id=1)

        self.assertEqual(post.title, 'Learning Python')

    def test_post_by(self):
        user = User.objects.get(id=1)
        post = Post.objects.get(author=user)

        self.assertEqual(post.title, 'Learning Python')

    def test_post_add_tags(self):
        post = Post.objects.get(id=1)
        tag1 = Tag(name="python", slug="python")
        tag2 = Tag(name="django", slug="django")
        post.tags = [tag1, tag2]
        post.save()

        self.assertEqual(len(post.tags), 2)


class SmokeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = create_default_user()

    def test_about(self):
        response = self.client.get('/blog/about/')
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.client.get('/blog/contact/')
        self.assertEqual(response.status_code, 200)

    def test_user_profile(self):
        response = self.client.get('/blog/profile/')
        print(response)
        self.assertRedirects(response,
                             "/login/?next=%2Fblog%2Fprofile%2F",
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True,
                             )

    def test_user_profile_with_login(self):
        self.client.login(username='testuser', password='rohlik123')
        response = self.client.get('/blog/profile/')
        print(response)
        self.assertEqual(response.status_code, 200)

    def add_comment_to_post(self):
        user = User.objects.get(id=1)
        post = Post(
            title="Learning Python",
            slug="learning-python",
            body="django, fastapi",
            status=Post.Status.PUBLISHED,
            author=user,
        )
        post.save()

        self.client.login(username='testuser', password='rohlik123')
        response = self.client.post('/1/comment/', {"body": "Very nice"})
        self.assertEqual(response.status_code, 200)