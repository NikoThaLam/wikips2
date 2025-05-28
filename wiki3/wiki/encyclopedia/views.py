from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content:
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "error not found real error no fake.",
            "title": title
        })

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()

    if util.get_entry(query):
        return redirect("entry", title=query)

    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()

        if util.get_entry(title):
            return render(request, "encyclopedia/create.html", {
                "error": "that already exists.",
                "title": title,
                "content": content
            })

        if not title or not content:
            return render(request, "encyclopedia/create.html", {
                "error": "u need title and content.",
                "title": title,
                "content": content
            })

        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/create.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("entry", title=title)

    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "u cant edit a page that doesnt exist",
            "title": title
        })

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    if entries:
        title = random.choice(entries)
        return redirect("entry", title=title)
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "not found error real no fake.",
            "title": "Random Page"
        })

### i had to search up most of this :sob: