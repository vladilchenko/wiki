from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entries/<str:title>/", views.show_entry, name="show_entry"),
    path("search/", views.search, name="search")
]
