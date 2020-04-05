"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.posts.views import home, posts, posts_new, post_view, post_edit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('posts/', posts),
    path('posts/new', posts_new),
    path('posts/<int:id>', post_view, name="post-view"),
    path('posts/edit/<int:id>', post_edit, name="post-edit"),
]
