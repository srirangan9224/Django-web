
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:proid>",views.profile_page,name="profile"),
    path("dp",views.dp,name="dp"),
    path("new",views.new,name="new"),
    path("comment",views.comment,name="comment"),
    path("follow",views.follow,name="follow"),
    
    #API route
    path("like",views.like,name="like")
]
