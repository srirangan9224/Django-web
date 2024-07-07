import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):
    if request.user.is_authenticated and not Profile.objects.filter(person=request.user):
        new_profile = Profile(person=request.user,dp="")
        new_profile.save()
        print(True)
    posts = Post.objects.all().order_by("-time")
    if not request.user.is_authenticated:
        profile = None
    else:
        profile = Profile.objects.filter(person=request.user).first()
    comments = Comment.objects.all()
    return render(request, "network/index.html",{
        "posts":posts,
        "user_profile": profile,
        "comments":comments
            })
@login_required
def profile_page(request,proid):
    user_profile = Profile.objects.filter(person=request.user).first()
    profile = Profile.objects.filter(pk=proid).first()
    posts = Post.objects.filter(profile=profile).order_by("-time")
    comments = Comment.objects.all()
    return render(request,"network/profile.html",{
        "profile":profile,
        "posts": posts,
        "user_profile":user_profile,
        "comments":comments
    })

def dp(request):
    if request.method == "POST":
        dp = request.POST["dp"]
        profile = Profile.objects.get(pk=request.POST["proid"])
        profile.dp = dp
        profile.save()
        return HttpResponseRedirect(reverse("profile",args=(int(request.POST["proid"]),)))
    
def new(request):
    if request.method == "POST":
        proid = int(request.POST["proid"])
        profile = Profile.objects.get(pk=request.POST["proid"])
        content = request.POST["content"]
        time = datetime.now()
        new_post = Post(
            profile=profile,
            content=content,
            time=time
        )
        new_post.save()
        print(proid)
        return HttpResponseRedirect(reverse("profile",args=(proid,)))
    
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")
    


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def comment(request):
    if request.method == "POST":
        post = Post.objects.get(pk=int(request.POST["post"]))
        person = request.user 
        content = request.POST["content"]
        new_comment = Comment(person=person,content=content,post=post)
        new_comment.save()
        return HttpResponseRedirect(reverse("index"))
    
@csrf_exempt
def like(request):
    if request.method == "POST":
        post = Post.objects.get(pk = int(json.loads(request.body)["post_id"]))
        if post.profile.person != request.user: 
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                print(post.likes.all())
            else:
                post.likes.add(request.user)
                return JsonResponse({"message": f"{request.user} liked post {post.content} by {post.profile.person}"}, status=201)
    else:
        return JsonResponse({"message":"post request required"},status=400)
    
def follow(request):
    if request.method == "POST":
        proid = int(request.POST["proid"])
        profile = Profile.objects.get(pk=proid)
        profile_2 = Profile.objects.filter(person=request.user).first()
        follow = request.POST["follow"]
        if follow == "follow":
            profile.follows.add(request.user)
            profile_2.following.add(profile.person)
        else:
            profile.follows.remove(request.user)
            profile_2.following.remove(profile.person)
        return HttpResponseRedirect(reverse("profile",args=(proid,)))