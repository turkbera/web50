from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createAuction, name="create"),
    path('auctions/<int:auction_id>/', views.auctionDetail, name='auctionDetail'),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("editAuction/<int:auction_id>", views.editAuction, name="editAuction"),
    path("myauctions/", views.myAuctions, name="myAuctions"),
    path("categories/", views.categoryList, name="categoryList"),
    path("categories/<str:category>/", views.categoryDetail, name="categoryDetail"),

]
