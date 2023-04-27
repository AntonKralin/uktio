from django.shortcuts import render
from django.http import HttpRequest
from .models import *


# Create your views here.
def index(request:HttpRequest):
    if request.method == "POST":
        user_name = request.POST.get('login', None)
        user_pass = request.POST.get("password", None)
        if user_name and user_pass:
               user_qset = Users.objects.filter(login=user_name, password=user_pass)
               if user_qset.exists():
                   user = user_qset.first()
                   request.session['user'] = user.id
                   return render(request, 'uktio/main.html')
        return render(request, 'uktio/index.html', context=
                        {'message': 'Wrong user or password'})
    else:
        return render(request, 'uktio/index.html')

def main(request:HttpRequest):
    return render(request, "uktio/main.html")

def about(request:HttpRequest):
    return render(request, "uktio/about.html")
