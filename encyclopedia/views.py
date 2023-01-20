from django.shortcuts import render
from markdown2 import Markdown 
from . import util
from django import forms
from django.contrib import messages
import random

class SearchForm(forms.Form):
    title = forms.CharField(label="", max_length= 10, min_length= 1, widget=forms.Textarea(attrs={
        "placeholder" : "Search by Title"
    }))

class NewEntryForm(forms.Form): 
    title = forms.CharField(label= "", max_length= 10, min_length= 1, widget=forms.TextInput(attrs={
        "placeholder" : "Title",
    }) )
    content = forms.CharField(label="",  max_length= 500, min_length=1, widget=forms.Textarea(attrs={
        "placeholder" : "This Wiki-like page uses Markdonw for writing the entries",

    }))
class EditEntryForm(forms.Form): 
    content = forms.CharField(label="", max_length=500, min_length=1, widget=forms.Textarea(attrs={
        "placeholder" : "This Wiki-like page uses Markdonw for writing the entries"
    }) )


markdowner = Markdown()

def index(request):
    context= { "entries" : util.list_entries(),
    "search": SearchForm()}
    return render(request, "encyclopedia/index.html", context)

def wikientry (request, title):
    #Check if the entry exist
    if util.get_entry(title) == None:
        #If doesn´t then redirects to an not found page
        return nonfound (request,title)
        #If it does, markdown converts the .md entry to an html for rendering
    return render (request, "encyclopedia/entry.html",{ 
        "entry" : markdowner.convert(util.get_entry(title)), "entrytitle" : title,
        "search": SearchForm(),
        })
    
    
def newentry (request):
    context= {"form" : NewEntryForm()}
    # If reached from link render the page
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html", context)

    elif request.method == "POST":
        form = NewEntryForm(request.POST)

        #If form is valid clean the form
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
        #Show error message if not valid
        else: 
            messages.error(request, 'Entry Form not valid, try again.')
            return render (request, "encyclopedia/newpage.html", {
                "newentry" : form
            })
        #Check for already existent entry, show error message if it does exist
        if util.get_entry (title):
            messages.error(request, 'This Entry already exist, try visitin the entry page on the wiki')
            return render (request, "encyclopedia/newpage.html", {
                "newentry" : form,
                "search": SearchForm(),
            })
        #Save the entry and redirect to that entry if success 
        else :
            util.save_entry(title, content)
            return wikientry(request,title)
def editentry (request, title):
    #If reached from link
    if request.method == "GET":
        #Get the entrty
        content= util.get_entry(title)
        #If not existing entry throws an error message
        if content == None:
            messages.error(request, "This entry doesn´t exist, and cannot be edited. Try creating a new entry")
        #If entry exist load the existent content for editing
        return render (request, "encyclopedia/editpage.html",{
            "title" : title,
            "editform": EditEntryForm(initial={"content":content}),
            "search": SearchForm(),
        } )
   
   #If reached from form
    elif request.method == "POST":
        form= EditEntryForm(request.POST)
      #Check if the form is valid
        if form.is_valid():
        #Clean content of the form for saving it in the updated entry
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return wikientry(request, title)



def nonfound (request, title): 
    return render (request, "encyclopedia/notfound.html", {
        "title" : title
    })

def randompage (request):
    #This uses a random module to select a random entry and then render with the wikientry function
    entries= util.list_entries()
    title= random.choice(entries)
    return wikientry(request,title)

def search (request):
    if request.method == "POST":
        form = SearchForm(request.POST)

    if form.is_valid():
        title= form.cleaned_data["title"]
        entry= util.get_entry(title)
        if entry:
            return wikientry(request,title)
        else:
            partialmatchs= partialmatchs(title)
            return render (request, "encyclopedia/search.html", {
                "title": title, 
                "partialmatchs" : partialmatchs,
                "searchform": SearchForm(),
            })

def partialmatchs (title):
    partialresults = []

    for entry in util.get_entry(title):
       if title.lower() in entry.lower() or entry.lower() in title.lower():
            partialresults.append(entry)
            return partialresults