from django.shortcuts import render
import re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry):
        html= markDown2Html(entry)
        title_match = re.search(r'^#\s*(.+)', util.get_entry(entry), re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        else:
            title = "Untitled"  # Default title if no heading is found
        return render(request, "encyclopedia/entry.html", {"entry": html, "title": title})
    else:
        render(request, "encyclopedia/error.html", {"error": "Entry not found"})

def markDown2Html(entry):
    html = util.get_entry(entry)
    #headings
    html = re.sub(r'^#\s*(.+)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^##\s*(.+)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^###\s*(.+)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    #bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    #unordered list
    html = re.sub(r'^\* *(.+)', r'<ul><li>\1</li></ul>', html, flags=re.MULTILINE)
    #link
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    #paragraph
    html = re.sub(r'^([^<\n].+)$', r'<p>\1</p>', html, flags=re.MULTILINE)
    return html