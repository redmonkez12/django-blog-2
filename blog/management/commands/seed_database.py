from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.apps import apps
from django.db import transaction
from taggit.models import Tag

from blog.models import Profile, Post


def create_default_user(username, password, email):
    user = User(
        username=username,
        email=email,
    )
    user.set_password(password)
    user.save()

    profile = Profile(user=user)
    profile.save()

    return user


def create_post(title, slug, body, status, user):
    post = Post(
        title=title,
        slug=slug,
        body=body,
        status=status,
        author=user,
    )
    post.save()

    return post


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        all_models = apps.get_models()

        for model in all_models:
            model.objects.all().delete()

        with transaction.atomic():
            tag1 = Tag(name="python", slug="python")
            tag2 = Tag(name="javascript", slug="javascript")
            tag3 = Tag(name=".net", slug="dotnet")
            tag1.save()
            tag2.save()
            tag3.save()

        with transaction.atomic():
            user1 = create_default_user("john", "john123", "john@gmail.com")
            user2 = create_default_user("alex", "ales123", "alex@gmail.com")
            user3 = create_default_user("olivia", "olivia123", "olivia@gmail.com")

            post1 = create_post("Learning Python", "learning-python", "django, fastapi", Post.Status.PUBLISHED, user1)
            post2 = create_post("Learning Javascript", "learning-javascript", "nextjs, react", Post.Status.PUBLISHED, user2)
            post3 = create_post("Learning .NET", "learning-net", "blazor, minimal api", Post.Status.PUBLISHED, user3)

            post1.tags.add(tag1)
            post1.save()

            post2.tags.add(tag2)
            post2.save()

            post3.tags.add(tag3)
            post3.save()
