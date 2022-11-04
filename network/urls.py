
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("<int:poster_id>/profile", views.profile, name="profile" ),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post"),

    path("posts", views.posts, name="posts"),
    path("post/<int:post_id>", views.post, name="post"),
    path("likes/<int:post_id>", views.likes, name="likes"),
    path("unlikes/<int:post_id>", views.unlike, name="unlike"),
    path("unfollow/<int:poster_id>", views.unfollow, name="unfollow"),
    path("follow/<int:poster_id>", views.follow, name="follow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
]