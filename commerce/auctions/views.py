from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from django import forms

class newListingForm(forms.Form):
    name = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10,decimal_places=2)
    description = forms.CharField(max_length=10000,widget=forms.Textarea)
    listing_date = forms.DateTimeField()
    image = forms.URLField()


def index(request):
    if request.method == "POST":
        
        listing_id = request.POST["listing_id"]

        if request.POST['bidder'] == "true" and request.POST['seller'] == "false":
            return HttpResponseRedirect(reverse("bidder",args=(listing_id,)))
        
        elif request.POST['bidder'] == "false" and request.POST['seller'] == "true":
            return HttpResponseRedirect(reverse("seller",args=(listing_id,)))
    try:
        if len(Watchlist.objects.filter(user=request.user)) != 0:
            watchlist = Watchlist.objects.filter(user=request.user).first()
            watchlist_count = len(watchlist.item.all())
        else:
            watchlist_count = 0
    except:
        watchlist_count = 0
    active_listings = Listing.objects.filter(sold=False)
    return render(request, "auctions/index.html",{
        "listings":active_listings,"user":request.user,
        "watchlist_count":watchlist_count
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
@login_required   
def bidder(request,listing_id):
    if len(Watchlist.objects.filter(user=request.user)) != 0:
        watchlist = Watchlist.objects.filter(user=request.user).first()
        watchlist_count = len(watchlist.item.all())
    else:
        watchlist_count = 0
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
        return HttpResponseRedirect(reverse("bidder",args=(listing_id,)))
    

    item = Listing.objects.get(pk=int(listing_id))
    comments = Comment.objects.filter(item=item)
    watchlist = Watchlist.objects.filter(user=request.user).first()
    in_watchlist = False


    try:
        if item in watchlist.item.all():
            in_watchlist = True
    except:
        pass


    categories = Category.objects.all()
    listing_cat = []


    for category in categories:
        if item in category.items.all():
            listing_cat.append(category)
    
    bids = Bid.objects.filter(item=item)
    bid_no = len(bids)
    max_bid = item.price
    max_bidder = request.user
    for bid in bids:
        if bid.bid > max_bid:
            max_bid = bid.bid
            max_bidder = bid.user
    max_bidder_check = False
    if max_bidder == request.user:
        max_bidder_check = True
    no_bid = False
    if max_bid == item.price:
        no_bid = True
    


    return render(request,"auctions/bidder.html",{
        "listing": item,
        "comments":comments,
        "in_watchlist":in_watchlist,
        "watchlist_count":watchlist_count,
        "listing_cat":listing_cat,
        "max_bid":max_bid,
        "bid_no": bid_no,
        "min_bid":max_bid+1,
        "max_bidder":max_bidder_check,
        "no_bid": no_bid,
        "sold": item.sold
    })


@login_required
def seller(request,listing_id):
    if len(Watchlist.objects.filter(user=request.user)) != 0:
        watchlist = Watchlist.objects.filter(user=request.user).first()
        watchlist_count = len(watchlist.item.all())
    else:
        watchlist_count = 0
    if request.method == "POST":
        category_id = request.POST["categories"]
        item = Listing.objects.get(pk=listing_id)
        category = Category.objects.get(pk=category_id)
        if item not in category.items.all():
            category.items.add(item)
    item = Listing.objects.get(pk=int(listing_id))
    comments = Comment.objects.filter(item=item)
    categories = Category.objects.all()
    listing_cat = []
    for category in categories:
        if item in category.items.all():
            listing_cat.append(category)

    bids = Bid.objects.filter(item=item)
    bid_no = len(bids)
    max_bid = item.price
    max_bidder = request.user

    for bid in bids:
        if bid.bid > max_bid:
            max_bid = bid.bid
    max_bidder_check = False
    if max_bidder == request.user:
        max_bidder_check = True
    no_bid = False
    if max_bid == item.price:
        no_bid = True
    bid_count = len(bids)

    return render(request,"auctions/seller.html",{
        "listing": item,
        "comments":comments,
        "watchlist_count":watchlist_count,
        "categories":categories,
        "listing_cat":listing_cat,
        "max_bid":max_bid,
        "max_bidder":max_bidder,
        "no_bid":no_bid,
        "bid_count":bid_count
    })

@login_required
def comment(request,listing_id):
    if request.method == "POST":
        link = request.POST["user"]
        content = request.POST["comment"]
        user = request.user
        item = Listing.objects.get(pk=int(listing_id))
        new_comment = Comment.objects.create(user=user,item=item,comment=content)
        new_comment.save()
        return HttpResponseRedirect(reverse(f"{link}",args=(listing_id,)))
    

@login_required   
def watchlist(request):
    if len(Watchlist.objects.filter(user=request.user)) != 0:
        watchlist = Watchlist.objects.filter(user=request.user).first()
        watchlist_count = len(watchlist.item.all())
    else:
        watchlist_count = 0
    user = request.user
    if len(Watchlist.objects.filter(user=user)) != 0:
        watchlist = Watchlist.objects.filter(user=user).first()
        listings = watchlist.item.all()
    else:
        listings = []
    return render(request,"auctions/watchlist.html",{
        "user":user,
        "listings":listings,
        "watchlist_count":watchlist_count
    })

@login_required
def category(request):
    if len(Watchlist.objects.filter(user=request.user)) != 0:
        watchlist = Watchlist.objects.filter(user=request.user).first()
        watchlist_count = len(watchlist.item.all())
    else:
        watchlist_count = 0
    categories = Category.objects.all()
    if request.method == 'POST':
        category = request.POST["categories"]
        if int(category) == 0:
            return render(request,"auctions/categories.html",{
                "watchlist_count":watchlist_count,
                "categories":categories
            })
        cat = Category.objects.get(pk=category)
        items = cat.items.all()
        return render(request,"auctions/categories.html",{
            "watchlist_count":watchlist_count,
            "categories":categories,
            "cat":cat,
            "items":items     
        })
    return render(request,"auctions/categories.html",{
        "watchlist_count":watchlist_count,
        "categories":categories
    })

@login_required
def create(request):
    if request.method == 'POST':
       name = request.POST["name"]
       description = request.POST["description"]
       price = request.POST["price"]
       listing_date = request.POST["listing_date"]
       image = request.POST["image"]
       category_id = request.POST["categories"]
       sold = False
       listed_by = request.user
       cat = Category.objects.get(pk=category_id)
       new_listing = Listing.objects.create(
           name=name,
           price=price,
           description=description,
           listing_date=listing_date,
           listed_by=listed_by,
           sold=sold,
           image=image
       )
       new_listing.save()
       cat.items.add(new_listing)
    if len(Watchlist.objects.filter(user=request.user)) != 0:
        watchlist = Watchlist.objects.filter(user=request.user).first()
        watchlist_count = len(watchlist.item.all())
    else:
        watchlist_count = 0
    user = request.user
    sold = False
    categories = Category.objects.all()
    return render(request,"auctions/create.html",{
        "watchlist_count":watchlist_count,
        "categories": categories,
        "form":newListingForm()
    })

@login_required
def bid(request):
    if request.method == 'POST':
        try:
            item = Listing.objects.get(pk=int(request.POST["listing_id"]))
            user = request.user
            bid = float(request.POST["bid"])
            new_bid = Bid.objects.create(
                item=item,
                user=user,
                bid=bid
            )
            new_bid.save()
            return HttpResponseRedirect(reverse(bidder,args=(int(request.POST["listing_id"]),)))
        except:
            raise Http404(request.POST)

def close(request):
    if request.method == "POST":
        item = Listing.objects.get(pk=int(request.POST["listing_id"]))
        item.sold = True
        listing_id = item.id
        item.save()


        bids = Bid.objects.filter(item=item)
        max_bid = item.price
        max_bidder = request.user
        for bid in bids:
            if bid.bid > max_bid:
                max_bid = bid.bid
        unsold = False
        if max_bid == item.price:
            unsold = True

        if unsold == False:
            max_bid_object = Bid.objects.filter(item=item,bid=max_bid).first()
            max_bidder = max_bid_object.user
            sale = Sold.objects.create(
                user=max_bidder,
                item=item
            )
                
        return HttpResponseRedirect(reverse("seller",args=(listing_id,)))
    
def purchases(request):
    if len(Watchlist.objects.filter(user=request.user)) != 0:
        watchlist = Watchlist.objects.filter(user=request.user).first()
        watchlist_count = len(watchlist.item.all())
    else:
        watchlist_count = 0


    purchases = Sold.objects.filter(user=request.user)
    purchased_products = []
    for purchase in purchases:
        purchased_products.append(purchase.item)

    return render(request,"auctions/purchases.html",{
        "watchlist_count":watchlist_count,
        "listings":purchased_products
    })