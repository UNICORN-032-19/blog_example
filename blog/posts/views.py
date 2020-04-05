from django.shortcuts import render, redirect
from blog.posts.models import Post
from django.http import HttpResponseNotAllowed
import math
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

DEFAULT_LIMIT = 1
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


def posts_new(request):
    if request.method == "GET":
        return render(
            request,
            'posts_new.html',
            context={}
        )
    elif request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("text")
        author = request.POST.get("author")
        post = Post.objects.create(title=title, text=text, author=author)
        post.save()
        return render(
            request,
            'posts_new.html',
            context={
                "message": f"New post {post.title} by {post.author} created",
                "message_type": "success",
            }
        )
    else:
        return HttpResponseNotAllowed()


def post_view(request, id):
    post = Post.objects.get(pk=id)
    return render(
        request,
        'post_view.html',
        context={"post": post}
    )


def post_edit(request, id):
    post = Post.objects.get(pk=id)
    if request.method == "GET":
        return render(
            request,
            'post_edit.html',
            context={"post": post}
        )
    elif request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("text")
        author = request.POST.get("author")
        post.title = title
        post.text = text
        post.author = author
        post.save()
        return redirect("post-view", id=post.id)
    else:
        return HttpResponseNotAllowed()
