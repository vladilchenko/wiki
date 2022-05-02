from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entry_urls()
    })


def show_entry(request, title: str):
    entry = util.get_entry(title)

    if entry:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title
        })
    else:
        return render(request, "encyclopedia/not_found.html",
        {
            "query": title
        }
    )


def search(request):
    if request.method == "POST":

        entries = util.list_entries()
        query = request.POST["query"]

        if query in entries:
            return HttpResponseRedirect(reverse("encyclopedia:show_entry", args=[query]))
        else:
            partial_matched_entries = util.list_entries_contained_query(query)
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "entries": partial_matched_entries
            })
    else:
        return HttpResponseRedirect(reverse("encyclopedia:index"))
