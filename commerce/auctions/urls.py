from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("bidder/<int:listing_id>",views.bidder,name="bidder"),
    path("seller/<int:listing_id>",views.seller,name="seller"),
    path("comment/<int:listing_id>",views.comment,name="comment"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("categories",views.category,name="categories"),
    path("create",views.create,name="create")
]
