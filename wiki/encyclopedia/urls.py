from django.urls import path
from . import views

urlpatterns = [
    path("",views.redirect,name="redirect"),
    path("wiki",views.index,name="index"),
    path("wiki/<str:name>",views.page,name="page"),
    path("wikinewPage",views.new,name="new"),
    path("wiki/random/random",views.random_page,name="random"),
    path("wiki/<str:name>/edit",views.edit,name="edit")
]