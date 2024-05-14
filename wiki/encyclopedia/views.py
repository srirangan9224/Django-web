from django.shortcuts import render
from . import util
from django.http import Http404


# Create your views here.
def index(request):
    return render(request,"encyclopedia/index.html",{"entries":util.list_entries()})

def page(request,name):
    if util.get_entry(name) != None:
        return render(request,"encyclopedia/page.html",{
            "name":name,
            "content":util.to_HTML(name)
        })
    else:
        raise Http404(f"this page does not exist.")
