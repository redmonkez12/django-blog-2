from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from taggit.models import Tag

from blog.forms import UserRegistrationForm, CommentForm, ProfileEditForm, ContactForm
from blog.models import Post, Profile, Comment


def post_list(request, tag_slug=None):
    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 2)
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
        {"posts": posts, "tag": tag},
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

        post_tags_ids = post.tags.values_list("id", flat=True)  # new
        similar_posts = Post.published.filter(
            tags__in=post_tags_ids
        ).exclude(id=post.id)
        similar_posts = similar_posts.annotate(
            same_tags=Count("tags")
        ).order_by("-same_tags", "-publish_at")[:4]

        form = CommentForm()
    except Post.DoesNotExist:
        raise Http404("No Post found.")
    return render(
        request,
        "post/detail.html",
        {
            "post": post,
            "form": form,
            "comments": comments,
            "similar_posts": similar_posts,
        }
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
    try:
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
            comment.user = request.user
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
    except Post.DoesNotExist:
        messages.error(
            request,
            "Invalid post."
        )
    except Exception:
        messages.error(
            request,
            "Cannot create comment. Please try again."
        )

    return redirect("blog:post_list")


@login_required
@require_POST
def delete_comment(request, id):
    try:
        comment = get_object_or_404(Comment, id=id, user=request.user)
        comment.delete()
        return HttpResponse("ok")
    except Exception:
        return HttpResponse("error", status=400)


@login_required
def user_profile(request):
    if request.method == "POST":
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if profile_form.is_valid():
            profile_form.save()

        return redirect("blog:post_list")
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, "account/settings.html", {"profile_form": profile_form})


def about(request):
    return render(request, "others/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            send_mail(
                f"Contact Form Submission from {name}",
                message,
                email,
                ["kayahots@gmail.com"],
                fail_silently=False,
            )

            return redirect("blog:contact_thank_you")
    else:
        form = ContactForm()

    return render(request, "others/contact.html", {"form": form})
