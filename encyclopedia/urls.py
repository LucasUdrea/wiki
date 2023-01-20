from django.urls import path

from . import views

app_name = "wiki"

urlpatterns =[
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wikientry, name="wikientry"),
    path("newentry", views.newentry, name= "newentry"),
    path("notfound", views.nonfound, name= "notfound"),
    path("edit/<str:title>", views.editentry, name="editentry"),
    path("randomentry", views.randompage, name="randomentry"),
    path("search", views.search, name="search")
]