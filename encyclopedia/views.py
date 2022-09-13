from django.shortcuts import render, HttpResponse, redirect

from . import util
import markdown2
import secrets

# Lists all pages.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Calls checkEntry to find out if the entry requested exists.  
def showEntry(request,title):
    if checkEntry(request,title) == False:
        return apology(f"Page does not exist.",404,request)
    else:
        htmlContent = mdToHtml(f'entries/{title}.md')
        return render(request, "encyclopedia/entry.html", {
        "htmlContent" : htmlContent,
        "title" : title
    })
    

# Checks to see whether an Entry exists or not.
def checkEntry(request, title):
    entries = util.list_entries()
    for entry in entries:
        if entry.lower() == title.lower():
            return True 
    return False

# Returns an apology page
def apology(message,code,request):
    return render(request, "encyclopedia/apology.html", {
        "code" : code,
        "message" : message
    })

# returns html content from a markdown file.
def mdToHtml(mdPath):
     entry = markdown2.markdown_path(mdPath)
     return entry

# returns the appropriate page according to the user's query 
# If the page is not found, show all entries with the query as a substring.
def search(request):
    if request.POST == {}:
        return apology("Server did not recieve a query.",404,request)
    query = request.POST['q']
    print("HERE")
    if checkEntry(request,query) == True:
        return redirect(f"wiki/{query}")
    else:
        entries = util.list_entries()
        suggestions = []
        for entry in entries:
            entryLower = entry.lower()
            found = entryLower.find(query.lower())
            print(found)
            if found != -1:
                suggestions.append(entry)
        return render(request, "encyclopedia/search.html", {
            "query" : query,
            "suggestions" : suggestions
        })

def editPage(request, markdownContent = None):
    return editor(request,False,request['content'])

# returns the page for editing or creating entries
def editor(request, new = True, markdownContent = None) :
    if markdownContent == None:
        return render(request, "encyclopedia/editor.html",{
        "new" : new,
        "markdownContent" : markdownContent
        })

def submitPage(request):
    title = request.POST['title']
    content = request.POST['content']

    # If the title does not already exist :
    title_exists = False
    entries = util.list_entries()
    for entry in entries:
        if title.lower() == entry.lower():
            title_exists = True
    if title_exists == False:
         util.save_entry(title,content)
         return index(request)
    else:
        return apology("The title you entered already exists.",403,request)

def submitEditedPage(request):
    title = request.POST['title']
    content = request.POST['content']
    util.save_entry(title,content)
    return showEntry(request, title)

def editPage(request):
    markdownContent = util.get_entry(request.POST["title"])
    return render(request, "encyclopedia/editor.html",{
        "markdownContent" : markdownContent,
        "title" : request.POST["title"]
    })


def random(request):
    entries = util.list_entries()
    return showEntry(request, secrets.choice(entries))