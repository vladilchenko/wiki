from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import util
from .forms import SearchForm


def index(request, form=None):

    form = SearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entry_urls(),
        "form": form
    })


def show_entry(request, title: str):
    entry = util.get_entry(title)
    form = SearchForm()
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title,
            "form": form
        })
    else:
        return render(request, "encyclopedia/not_found.html",
        {
            "query": title,
            "form": form
        }
    )


def search(request):
    if request.method == "POST":

        form = SearchForm(request.POST)
        if form.is_valid():

            entries = util.list_entries()
            query = form.cleaned_data["query"]

            if query in entries:
                return HttpResponseRedirect(reverse("encyclopedia:show_entry", args=[query]))
            else:
                partial_matched_entries = util.list_entries_contained_query(query)
                return render(request, "encyclopedia/search.html", {
                    "query": query,
                    "entries": partial_matched_entries,
                    "form": form
                })
        else:
            return HttpResponseRedirect(reverse("encyclopedia:index"))
    else:
        return HttpResponseRedirect(reverse("encyclopedia:index"))
