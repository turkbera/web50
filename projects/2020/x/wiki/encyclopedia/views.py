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
def markDown2Html(entry):
    html = util.get_entry(entry)
    #headings
    # Handle headings
    html = re.sub(r'^(#+)\s*(.+)', r'<h1>\2</h1>', html, flags=re.MULTILINE)    
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

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title of New Entry", widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={"class": "form-control"}))

    def is_valid(self):
        valid = super().is_valid()
        if valid:
            title = self.cleaned_data.get('title')
            content = self.cleaned_data.get('content')
            title_match = (re.search(r'^#\s*(.+)', content, re.MULTILINE))
            print(title)
            print(title_match)
            if not re.search(r'^#\s+.+', content, re.MULTILINE):
                self.add_error('content', 'The content must start with a Markdown heading (# ) and additional whitespace')
                return False
            if title.strip() != title_match.group(1).strip():
                self.add_error('content', 'The title in the title part and markdown part should match!')
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
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
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

class editEntryForm(forms.Form):
    content = forms.CharField(label="",widget=forms.Textarea(attrs={"class":"form-control"}))

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        return content



def editPage(request, entry):
    entry = entry.strip()
    if request.method == "POST":
        form = editEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content'].strip()
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry]))
    else:
        content = util.get_entry(entry)
        form = editEntryForm(initial={'content': content})
    
    return render(request, "encyclopedia/editPage.html", {
        "form": form,
        "entry": entry
    })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    results = [entry for entry in entries if query.lower() in entry.lower()]
    
    if query.lower() in [entry.lower() for entry in entries]:
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=[query]))
    
    return render(request, "encyclopedia/search.html", {
        "entries": results,
    })