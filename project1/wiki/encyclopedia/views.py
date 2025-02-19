from django.http import HttpResponse
from markdown2 import Markdown
from django.shortcuts import redirect, render
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    markdowner = Markdown()
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/not_found.html")
    content_convrted = markdowner.convert(content)
    return render(
        request,
        "encyclopedia/entry.html",
        {"title": title, "content": content_convrted},
    )


def search(request):
    query = request.GET.get("q")

    if query:
        entry_content = util.get_entry(query)

        if entry_content:
            return redirect("encyclopedia:entry", title=query)
        else:
            entries = [
                title for title in util.list_entries() if query.lower() in title.lower()
            ]

            return render(
                request,
                "encyclopedia/search_results.html",
                {"entries": entries, "query": query},
            )
    else:
        return render(
            request,
            "encyclopedia/search_results.html",
            {
                "entries": [],
                "query": query,
                "error_message": "Please enter a search query in the search box.",
            },
        )


def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title):
            return render(
                request,
                "encyclopedia/create.html",
                {
                    "error_message": "An encyclopedia entry with this title already exists. Please choose a different title.",
                    "title": title,
                    "content": content,
                },
            )
        else:
            util.save_entry(title, content)
            return redirect("encyclopedia:entry", title=title)

    return render(request, "encyclopedia/create.html")


def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")

        util.save_entry(title, content)
        return redirect(
            "encyclopedia:entry", title=title
        )

    entry_content = util.get_entry(title)
    if entry_content is None:
        return render(request, "encyclopedia/edit.html", {"error_message": "Entry not_found for editing."})

    return render(
        request,
        "encyclopedia/edit.html",
        {
            "title": title,
            "content": entry_content,
        },
    )


def random_page(request):
    entries = util.list_entries()  # Get a list of all entry titles
    random_entry_title = random.choice(entries)  # Choose a random title
    return redirect("encyclopedia:entry", title=random_entry_title)  # Redirect
