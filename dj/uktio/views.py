from django.shortcuts import render
from django.http import HttpRequest


# Create your views here.
def index(request:HttpRequest):
    return render(request, 'uktio/index.html')    

def main(request:HttpRequest):
    return render(request, "uktio/main.html")

def about(request:HttpRequest):
    return render(request, "uktio/about.html")
