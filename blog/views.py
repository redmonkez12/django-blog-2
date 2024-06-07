from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_POST

from blog.forms import UserRegistrationForm, CommentForm
from blog.models import Post, Profile


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
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
        comments = post.comments.filter(active=True)

        form = CommentForm()
    except Post.DoesNotExist:
        raise Http404("No Post found.")
    return render(
        request,
        "post/detail.html",
        {"post": post, "form": form, "comments": comments}
    )


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, "account/register_done.html", {"user_form": user_form})
    else:
        user_form = UserRegistrationForm()

    return render(request, "account/register.html", {"form": user_form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.profile = request.user.profile
        comment.save()

    return render(
        request,
        "post/comment.html",
        {
            "post": post,
            "form": form,
            "comment": comment
        }
    )
