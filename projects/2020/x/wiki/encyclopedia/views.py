from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import redirect
import re
import random
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
        return render(request, "encyclopedia/newPage.html", {
            "form":NewEntryForm()
        })
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

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title of New Entry")
    content = forms.CharField(widget=forms.Textarea)

    def is_valid(self):
        valid = super().is_valid()
        if valid:
            content = self.cleaned_data.get('content')
            if not re.search(r'^#\s+.+', content, re.MULTILINE):
                self.add_error('content', 'The content must contain a Markdown heading (#)')
                return False
        return valid


def newPage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['title'] in util.list_entries():
                form.add_error('title', 'This title already exists.')
                return render(request, "encyclopedia/newPage.html", {
                "form": form
                })            
            else:
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[content]))
        else:
            return render(request, "encyclopedia/newPage.html", {
                "form": form
                })
    else:
        return render(request, "encyclopedia/newPage.html", {
            "form": NewEntryForm()
        })

def randomPage(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=(random_entry,)))