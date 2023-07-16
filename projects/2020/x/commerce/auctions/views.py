from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all()
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

def createAuction(request):
    if request.method =="POST":
        name = request.POST["name"]
        price = request.POST["price"]
        description = request.POST["description"]
        user_id = request.user
        imageUrl = request.POST["imageUrl"]
        try:
            auction = Auction(name=name, price = price, user = user_id, description = description, imageUrl = imageUrl)
        except IntegrityError:
            return render(request, "auctions/create.html", {
                "message": "Auction name already taken."
            })
        auction.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")
    

def auctionDetail(request, auction_id):
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        auction = None

    if not auction:
        return render(request, "auctions/auctionDetail.html", {
            "message": "Auction not found.",
            "comments": Comment.objects.all()
        })

    if request.method == "POST":
        if "bid-submit" in request.POST:
            bid = int(request.POST.get("bid", 0))
            bidMo = Bid(auction=auction, bid=bid, user=request.user)
            bidMo.save()
            if bid > auction.price:
                auction.price = bid
                auction.save()
                return render(request, "auctions/auctionDetail.html", {
                    "auction": auction,
                    "message": "Currently, you are winning the bid.",
                    "comments": Comment.objects.all()
                })
            else:
                return render(request, "auctions/auctionDetail.html", {
                    "auction": auction,
                    "message": "Bid is not greater than the current price.",
                    "comments": Comment.objects.all()
                })
        elif "comment-submit" in request.POST:
            commentText = request.POST.get("comment")
            comment = Comment(auction=auction, comment=commentText, user=request.user)
            comment.save()
            return render(request, "auctions/auctionDetail.html", {
                "auction": auction,
                "message": "Comment added successfully.",
                "comments": Comment.objects.all()
            })

    return render(request, "auctions/auctionDetail.html", {
        "auction": auction,
        "comments": Comment.objects.all()
    })
