from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"{self.user.username}"


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="blog_posts"
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-publish_at"]
        indexes = [
            models.Index(fields=["-publish_at"]),
        ]

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[
                self.publish_at.year,
                self.publish_at.month,
                self.publish_at.day,
                self.slug
            ]
        )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Comment by {self.profile.user.username} on {self.post}"
