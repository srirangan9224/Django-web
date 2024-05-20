from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    if request.method == "POST":
        
        listing_id = request.POST["listing_id"]

        if request.POST['bidder'] == "true" and request.POST['seller'] == "false":
            return HttpResponseRedirect(reverse("bidder",args=(listing_id,)))
        
        elif request.POST['bidder'] == "false" and request.POST['seller'] == "true":
            return HttpResponseRedirect(reverse("seller",args=(listing_id,)))
        
    active_listings = Listing.objects.filter(sold=False)
    return render(request, "auctions/index.html",{
        "listings":active_listings,"user":request.user
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
   
def bidder(request,listing_id):
    if request.method == 'POST':
        present = request.POST["present"]
        item = Listing.objects.get(pk=listing_id)
        user = request.user
        if present == "true":
            if len(Watchlist.objects.filter(user=user)) == 0:
                new_watchlist = Watchlist.objects.create(user=user)
                new_watchlist.save()
                new_watchlist.item.add(item)
                print(new_watchlist.item)
            else:
                watchlist = Watchlist.objects.filter(user=user).first()
                watchlist.item.add(item)
        elif present == "false":
            watchlist = Watchlist.objects.filter(user=user).first()
            watchlist.item.remove(item)
    item = Listing.objects.get(pk=int(listing_id))
    comments = Comment.objects.filter(item=item)
    watchlist = Watchlist.objects.filter(user=request.user).first()
    in_watchlist = False
    try:
        if item in watchlist.item.all():
            in_watchlist = True
    except:
        raise Http404(watchlist.item)
    return render(request,"auctions/bidder.html",{
        "listing": item,
        "comments":comments,
        "in_watchlist":in_watchlist
    })

def seller(request,listing_id):
    item = Listing.objects.get(pk=int(listing_id))
    comments = Comment.objects.filter(item=item)
    return render(request,"auctions/seller.html",{
        "listing": item,
        "comments":comments
    })

def comment(request,listing_id):
    if request.method == "POST":
        link = request.POST["user"]
        content = request.POST["comment"]
        user = request.user
        item = Listing.objects.get(pk=int(listing_id))
        new_comment = Comment.objects.create(user=user,item=item,comment=content)
        new_comment.save()
        return HttpResponseRedirect(reverse(f"{link}",args=(listing_id,)))
    
def watchlist(request):
    user = request.user
    if len(Watchlist.objects.filter(user=user)) != 0:
        watchlist = Watchlist.objects.filter(user=user).first()
        listings = watchlist.item.all()
    else:
        listings = []
    return render(request,"auctions/watchlist.html",{
        "user":user,
        "listings":listings
    })