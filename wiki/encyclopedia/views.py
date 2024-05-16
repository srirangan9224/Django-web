from django.shortcuts import render
from . import util
import os
from django.urls import reverse
from django.http import Http404,HttpResponseRedirect,HttpResponse
from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content",widget=forms.Textarea)

# Create your views here.
def redirect(request):
    return HttpResponseRedirect(reverse("index"))


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

def new(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if util.get_entry(title) == None:
            file = open(rf"c:\Users\Hp\Desktop\web\entries\{title}.md",'w')
            file.write(content)
            file.close()
            return HttpResponseRedirect(reverse("page",args=(title,)))
        else:
            raise Http404("page already exists")
    return render(request,"encyclopedia/new.html",{
        "form":NewPageForm()
    })

def random_page(request):
    page = util.random_page()
    return HttpResponseRedirect(reverse("page",args=(page,)))

def edit(request,name):
    ...
