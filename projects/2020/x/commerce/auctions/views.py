from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, Auction, Bid, Comment, Watchlist


def index(request):
    activeAuctions = Auction.objects.filter(isOpen=True)
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all(),
        "activeAuctions": activeAuctions
    })

def closedAuctions(request):
    closedAuctions = Auction.objects.filter(isOpen=False)
    print(closedAuctions)
    return render(request, "auctions/closedAuctions.html", {
        "auctions": Auction.objects.all(),
        "closedAuctions": closedAuctions
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
    categories = Auction.CATEGORY_CHOICES
    if request.method =="POST":
        name = request.POST["name"]
        price = request.POST["price"]
        description = request.POST["description"]
        user_id = request.user
        imageUrl = request.POST["imageUrl"]
        category = request.POST["category"]
        if not name or not price:
            return render(request, "auctions/create.html", {
                "message": "Name and price are required fields."
            })
        try:
            auction = Auction(name=name, price = price, user = user_id, description = description, imageUrl = imageUrl, category=category)
        except IntegrityError:
            return render(request, "auctions/create.html", {
                "message": "Auction name already taken."
            })
        auction.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        print(categories)
        return render(request, "auctions/create.html", {
            "categories": categories        
            })
    

def auctionDetail(request, auction_id):
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        auction = None
    if not auction:
        return render(request, "auctions/auctionDetail.html", {
            "message": "Auction not found.",
            "comments": Comment.objects.all(),
        })
    last_bid = Bid.objects.filter(auction=auction).order_by("-timestamp").first()
    watchlistItems = Watchlist.objects.filter(user=request.user) 
    auctions = []
    for item in watchlistItems:
        auctions.extend(item.auction.all())
    if request.method == "POST":
        watchlistItems = Watchlist.objects.filter(user=request.user) 
        auctions = []
        for item in watchlistItems:
            auctions.extend(item.auction.all())
        if "bid-submit" in request.POST:
            bid = int(request.POST.get("bid", 0))
            bidMo = Bid(auction=auction, bid=bid, user=request.user)
            bidMo.save()
            last_bid = Bid.objects.filter(auction=auction).order_by("-timestamp").first()
            if last_bid and not last_bid.is_accepted:
            # Handle the case where there is no accepted bid or no bid at all
                last_bid = None
            print(last_bid)
            if bid > auction.price:
                auction.price = bid
                auction.save()
                return render(request, "auctions/auctionDetail.html", {
                    "auction": auction,
                    "message": "Yuppi, you made the best offer.",
                    "comments": Comment.objects.all(),
                    "watchlistItems": auctions,
                    "winner":last_bid
                })
            else:
                print("Bid is not greater than the current price.")
                return render(request, "auctions/auctionDetail.html", {
                    "auction": auction,
                    "message": "Bid is not greater than the current price.",
                    "comments": Comment.objects.all(),
                    "watchlistItems": auctions,
                    "winner":last_bid
                })
        elif "comment-submit" in request.POST:
            commentText = request.POST.get("comment")
            comment = Comment(auction=auction, comment=commentText, user=request.user)
            comment.save()
            return render(request, "auctions/auctionDetail.html", {
                "auction": auction,
                "message": "Comment added successfully.",
                "comments": Comment.objects.all(),
                "watchlistItems": auctions,
                "winner":last_bid
            })
        elif "watchlist-submit" in request.POST:
            watchlist = Watchlist.objects.create(user = request.user)
            watchlist.auction.add(auction)
            watchlist.save()
            watchlistItems = Watchlist.objects.filter(user=request.user) 
            auctions = []
            for item in watchlistItems:
                auctions.extend(item.auction.all())
            return render(request, "auctions/auctionDetail.html", {
            "auction": auction,
            "message": "Added to watchlist.",
            "comments": Comment.objects.all(),
            "watchlistItems": auctions,
            "winner":last_bid
            })
        elif "watchlist-delete" in request.POST:
            watchlist = Watchlist.objects.get(user = request.user, auction=auction)
            watchlist.auction.remove(auction)
            watchlistItems = Watchlist.objects.filter(user=request.user) 
            auctions = []
            for item in watchlistItems:
                auctions.extend(item.auction.all())
            print(auctions)
            return render(request, "auctions/auctionDetail.html", {
            "auction": auction,
            "message": "Deleted from wathclist.",
            "comments": Comment.objects.all(),
            "watchlistItems": auctions,
            "winner":last_bid
            })
        elif "close-auction" in request.POST:
            if auction.user == request.user:
                auction.isOpen = False
                auction.save()
                last_bid = Bid.objects.filter(auction=auction).order_by("-timestamp").first()
                return render(request, "auctions/auctionDetail.html", {
                        "auction": auction,
                        "comments": Comment.objects.all(),
                        "message": "Auction is closed.",
                        "watchlistItems": auctions,
                        "winner":last_bid
                    })

    return render(request, "auctions/auctionDetail.html", {
        "auction": auction,
        "comments": Comment.objects.all() ,
        "winner":last_bid,
        "watchlistItems":auctions
        })

@login_required
def watchlist(request):
    watchlistItems = Watchlist.objects.filter(user=request.user)
    auctions = []
    for item in watchlistItems:
        auctions.extend(item.auction.all())
    return render(request, "auctions/watchlist.html", {
        "watchlistItems": auctions
    })
@login_required
def editAuction(request, auction_id):
    categories = Auction.CATEGORY_CHOICES
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        auction = None

    # Check if the auction exists and if the user is the creator
    if not auction or auction.user != request.user:
        return render(request, "auctions/error.html", {
            "message": "Auction not found or you are not the creator."
        })

    if request.method == "POST":
        # Check if the user clicked the delete button
        if "delete" in request.POST:
            auction.delete()
            return HttpResponseRedirect(reverse("index"), {
                "message" : "Auction Deleted"
            })

        # Update the auction details
        auction.name = request.POST["name"]
        auction.price = request.POST["price"]
        auction.description = request.POST["description"]
        auction.imageUrl = request.POST["imageUrl"]
        auction.category = request.POST["category"]
        auction.save()
        return HttpResponseRedirect(reverse("auctionDetail", args=[auction.id]))

    return render(request, "auctions/editAuction.html", {
        "auction": auction,
        "categories":categories
    })
@login_required
def myAuctions(request):
    userAuctions = Auction.objects.filter(user=request.user)
    return render(request, "auctions/myAuctions.html", {"userAuctions": userAuctions})

def categoryList(request):
    categories = Auction.CATEGORY_CHOICES
    return render(request, "auctions/categoryList.html", {"categories": categories})

def categoryDetail(request, category):
    listings = Auction.objects.filter(category=category)
    return render(request, "auctions/categoryDetail.html", {"category": category, "auctions": listings})