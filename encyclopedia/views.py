from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import random

from . import util
from .forms import SearchForm, CreateEntryForm, EditEntryForm


def index(request, form=None):

    form = SearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entry_urls(),
        "form": form
    })


def show_entry(request, title: str):
    title = title.replace("_", " ")
    entry = util.get_entry(title)
    html_entry = util.process_entry(entry)
    form = SearchForm()
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "entry": html_entry,
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


def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:show_entry", args=[title]))


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

def create_entry(request):
    if request.method == "GET":
        form = CreateEntryForm()
        search_form = SearchForm()
        return render(request, "encyclopedia/create_entry.html", {
            "form": search_form,
            "add_entry_form": form
        })
    elif request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:show_entry", args=[title]))
        else:
            search_form = SearchForm()
            return render(request, "encyclopedia/create_entry.html", {
                "add_entry_form": form,
                "form": search_form
            })

def edit_entry(request):
    if request.method == "GET":

        title = request.GET.get("title")
        content = util.get_entry(title)

        data = {
            "title": title,
            "content": content
        }

        form = EditEntryForm(data)
        search_form = SearchForm()

        return render(request, "encyclopedia/edit_entry.html", {
            "form": search_form,
            "add_entry_form": form
        })
    elif request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:show_entry", args=[title]))
        else:
            search_form = SearchForm()
            return render(request, "encyclopedia/edit_entry.html", {
                "add_entry_form": form,
                "form": search_form
            })
