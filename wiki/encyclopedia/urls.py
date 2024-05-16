from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("/<str:name>",views.page,name="page"),
    path("newPage",views.new,name="new"),
    path("/random/random",views.random_page,name="random")
]