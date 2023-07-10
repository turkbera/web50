from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("newEntry", views.newPage, name= "newPage"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("randomPage/", views.randomPage, name="randomPage"),
    path("edit/<str:entry>", views.editPage, name="editPage"),
    path("search", views.search, name="search"),
    ]
