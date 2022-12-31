from django.shortcuts import render
from markdown2 import Markdown
from django import forms
markdowner=Markdown()
import markdown
from . import util
import random


class NewPageForm(forms.Form):
    title=forms.CharField(widget=forms.TextInput, label="Title")
    content=forms.CharField(widget=forms.Textarea, label="Content")  

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convert_md_to_html(title):
    content=util.get_entry(title)
    if content == None:
        return None
    else:
        return Markdown().convert(content)
def convert(request,title):
    html_content=convert_md_to_html(title)
    
    if html_content == None:
        return render(request, "encyclopedia/nonExisting.html",{
            "message":"This entry does not exist"
        })        
    else:
        
        context={
            "title":title,
            "content":html_content
            
        }
        
        return render(request, "encyclopedia/entry.html",context)

def search(request):
    if request.method=="POST":
        entry_search=request.POST['q']
        html_content=convert_md_to_html(entry_search)
        if html_content is not None:
            context={
                "title":entry_search,
                "content": html_content
            }
            return render(request,"encyclopedia/entry.html",context)
        else:
            svi=util.list_entries()
            preporuke=[]
            for svaki in svi:
                if entry_search.lower() in svaki.lower():
                    preporuke.append(svaki)
           
            return render(request, "encyclopedia/search.html",
            {
                "preporuke":preporuke
            })


def new(request):
    return render (request,"encyclopedia/new.html")

def save(request):
    if request.method=="POST":
        entry_title=request.POST['title']
        content=request.POST['content']
        entries=util.list_entries()
        if entry_title in entries:
            return render(request,"encyclopedia/alreadyExists.html")
        else:
            util.save_entry(entry_title,content)
            html=convert_md_to_html(entry_title)
            context={
                "title":entry_title,
                "content":html
            }
            return render(request,"encyclopedia/entry.html",context)

def rand(request):
    arr=util.list_entries()
    entry_title=random.choice(arr)
    html=convert_md_to_html(entry_title)
    context={
        "title":entry_title,
        "content":html
    }
    return render(request,"encyclopedia/entry.html",context)
    

def edit(request):
    if request.method=="POST":
        input_title=request.POST['title']
        text=convert_md_to_html(input_title)
        context={
        "title":input_title,
        "content":text
    }
    return render(request,"encyclopedia/edit.html",context)

def save_edit(request):
    if request.method=='POST':
        input_title=request.POST['title']
        input_content=request.POST['content']
        util.save_entry(input_title,input_content)
        html=convert_md_to_html(input_title)
        context={
            "title":input_title,
            "content":html
            }
        return render(request,"encyclopedia/entry.html",context)