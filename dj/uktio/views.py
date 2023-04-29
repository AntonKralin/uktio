from django.shortcuts import render
from django.http import HttpRequest, HttpResponseNotFound
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
                   context = {"user": user}
                   return render(request, 'uktio/main.html', context=context)
        del request.session['user']
        return render(request, 'uktio/index.html', 
                        {'message': 'Wrong user or password'})
    else:
        del request.session['user'] 
        return render(request, 'uktio/index.html')

def main(request:HttpRequest):
    user_id = request.session.get('user', None)
    user = None
    if user_id:
        user = Users.objects.get(id=user_id)
    else:
        return HttpResponseNotFound("<h1>No user</h1>")
        
    
    context = {"user": user}
    return render(request, 'uktio/main.html', context=context)

def about(request:HttpRequest):
    return render(request, "uktio/about.html")
