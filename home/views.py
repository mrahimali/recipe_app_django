from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    people=[
        {"name":"Rahim", "age":27},
        {"name":"Raqim", "age":24},
        {"name":"Aquib", "age":10},
        {"name":"shadab", "age":32}
    ]


    return render(request, 'home/index.html', context={'people':people})


def success_page(req):
    return HttpResponse("<h1 style='color:red'>This is succes page</h1>")

def contact(req):
    return render(req, 'home/contact.html')

def about(req):
    return render(req, 'home/about.html')

