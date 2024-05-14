from django.shortcuts import render
from . import util
from django.urls import reverse
from django.http import Http404,HttpResponseRedirect


# Create your views here.
def index(request):
    if request.method == "POST":
        sub = request.POST['q']
        match = util.search(sub)
        return render(request,"encyclopedia/results.html",{"match":match})

    return render(request,"encyclopedia/index.html",{"entries":util.list_entries()})

def page(request,name):
    if util.get_entry(name) != None:
        return render(request,"encyclopedia/page.html",{
            "name":name,
            "content":util.to_HTML(name)
        })
    else:
        raise Http404(f"this page does not exist.")
