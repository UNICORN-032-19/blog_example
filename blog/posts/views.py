from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from blog.posts.models import Post
from django.http import HttpResponseNotAllowed
import math
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from blog.posts.forms import PostForm, EditPostForm
from datetime import datetime

DEFAULT_LIMIT = 5
DEFAULT_OFFSET = 0


def get_link(page, search):
    result = f"/posts/?page={page}"
    if search:
        result = f"{result}&q={search}"
    return result


def home(request):
    return render(
        request,
        'home.html',
        context={}
    )


@login_required
def posts(request):
    search = request.GET.get("q")
    page = request.GET.get("page")
    if page is None and not search:
        return redirect(get_link(1, search))
    page = int(page or 1)
    limit = DEFAULT_LIMIT
    offset = (page - 1) * limit
    if not search:
        posts = Post.objects.all()
    else:
        vector = SearchVector('text', weight='A') + SearchVector('title', weight='B')
        query = SearchQuery(search)
        posts = Post.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('rank')
    count = len(posts)
    posts = posts[offset:offset+limit]

    pages = math.ceil(count / limit)
    previous_page = False
    next_page = False
    if page > 1:
        previous_page = get_link(page-1, search)
    if page < pages:
        next_page = get_link(page+1, search)
    pages_links = {x+1: {"link": get_link(x+1, search), "disabled": False} for x in range(pages)}
    if page in pages_links:
        pages_links[page]["disabled"] = True
    return render(
        request,
        'posts.html',
        context={
            "posts": posts,
            "previous_page": previous_page,
            "next_page": next_page,
            "pages": pages,
            "pages_links": pages_links,
        }
    )


@login_required
@permission_required('posts.can_create_post')
def posts_new(request):
    base_context = {"new_post": PostForm()}
    if request.method == "GET":
        return render(
            request,
            'posts_new.html',
            context=dict(**base_context, **{})
        )
    elif request.method == "POST":
        form = PostForm(request.POST)
        post = form.save()
        if request.user.is_authenticated:
            post.create_uid = request.user
            post.save()
        return render(
            request,
            'posts_new.html',
            context=dict(**base_context, **{
                "message": f"New post {post.title} by {post.author} created",
                "message_type": "success",
            })
        )
    else:
        return HttpResponseNotAllowed()


@login_required
def post_view(request, id):
    post = Post.objects.get(pk=id)
    return render(
        request,
        'post_view.html',
        context={"post": post}
    )


@login_required
def post_edit(request, id):
    post = Post.objects.get(pk=id)
    form = EditPostForm(instance=post)
    if request.method == "GET":
        return render(
            request,
            'post_edit.html',
            context={"form": form}
        )
    elif request.method == "POST":
        create_uid = post.create_uid
        created_at = post.created_at
        form = PostForm(request.POST)
        post = form.save()
        post.updated_at = datetime.now()
        if request.user.is_authenticated:
            post.update_uid = request.user
        post.create_uid = create_uid
        post.created_at = created_at
        post.save()
        return redirect("post-view", id=post.id)
    else:
        return HttpResponseNotAllowed()
