from django.shortcuts import render
from markdown2 import Markdown
markdower = Markdown()
import markdown
import random

from . import util 

def convert_to_html(title):
    content = util.get_entry(title)
    markdower = Markdown()
    if content==None:
        return None
    else :
        markdower.convert(content)

    return content    

def index(request): 
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_Page = util.get_entry(title)
    if entry_Page is None:
        return render(request, "encyclopedia/error.html",{
            "entryTitle": title
        })
    else :
        return render(request, "encyclopedia/entry.html", {
            "entryTitle": title ,
            "entry": convert_to_html(title)
        })

def search(request):
    if request.method == 'GET':
        input = request.GET.get('q')
        entries = util.list_entries()
        html = convert_to_html(input)
        search_pages = []
        
        for entry in entries:
            if input.upper() in entry.upper():
                search_pages.append(entry)

        for entry in entries:
            if input.upper() == entry.upper():
                return render (request, "encyclopedia/entry.html",{
                    "entryTitle": input,
                    "entry": html
                })
                    
            elif search_pages !=[]:
                return render (request, "encyclopedia/search.html",{
                    "entries": search_pages
                })
            
            else :
                return render (request, "encyclopedia/error.html",{
                    "entryTitle":input
                })
 
def newPage(request):
    return render(request, "encyclopedia/newPage.html")

def save(request):
    if request.method == 'POST':
        input_title = request.POST['title']
        input_text = request.POST['text']
        entries = util.list_entries()
        html= convert_to_html(input_title)

        Already_exist_true='false'
        for entry in entries:
            if input_title.upper() == entry.upper():
              Already_exist_true = 'true'

        if Already_exist_true == 'true':
                return render(request, "encyclopedia/already_exist.html", {
                    "entryTitle": input_title,
                    "entry": html
                }) 

        else:
            util.save_entry(input_title, input_text)
            return render(request, "encyclopedia/entry.html",{
                "entryTitle":input_title,
                "entry":html
            })    


def randomPage(request):
    entries=util.list_entries()
    randEntry=random.choices(entries)
    html=convert_to_html(randEntry)
    return render(request, "encyclopedia/entry.html",{
        "entry":randEntry,
        "entryTitle":html
    })


def editPage(request):
    if request.method=='POST':
        input_title = request.POST['title']
        text= util.get_entry(input_title)

        return render(request, "encyclopedia/editPage.html",{
            "entry":text,
            "entryTitle":input_title
        })
    

def saveEdits(request):
    if request.method == 'POST':
        entryTitle = request.POST['title']    
        entry = request.POST['text']
         
        util.save_entry(entryTitle, entry)
         
        html = convert_to_html(entryTitle)
        return render(request, "encyclopedia/entry.html",{
            "entryTitle":entryTitle,
            "entry":html
        })