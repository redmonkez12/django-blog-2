from django.shortcuts import render
from django.http import Http404

from blog.models import Post


def post_list(request):
    posts = Post.published.all()
    return render(
        request,
        "post/list.html",
        {"posts": posts}
    )


def post_detail(request, year, month, day, post):
    try:
        post = Post.published.get(
            slug=post,
            publish_at__year=year,
            publish_at__month=month,
            publish_at__day=day
        )
    except Post.DoesNotExist:
        raise Http404("No Post found.")
    return render(
        request,
        "post/detail.html",
        {"post": post}
    )