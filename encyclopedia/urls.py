from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entries/<str:title>/", views.show_entry, name="show_entry"),
    path("search/", views.search, name="search"),
    path("add/", views.create_entry, name="create_entry"),
    path("edit_entry/", views.edit_entry, name="edit_entry"),
    path("random/", views.random_page, name="random_page")
]
