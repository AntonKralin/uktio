from django.shortcuts import render
from django.http import HttpRequest, HttpResponseNotFound
from .models import *


# Create your views here.
def index(request:HttpRequest):
    if request.session.get('user', None):
        user_id = request.session.get('user', None)
        user = None
        if user_id:
            user = Users.objects.get(id=user_id)
        else:
            return HttpResponseNotFound("<h1>No user</h1>")
        context = {"user": user}
        return render(request, 'uktio/main.html', context=context)
    
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
        return render(request, 'uktio/index.html', 
                        {'message': 'Wrong user or password'})
    else:
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

def region(request:HttpRequest):
    return render(request, 'uktio/region.html')

def edit_region(request:HttpRequest, id:int):
    try:
        region = Region.objects.get(id=id)
        if request.method == "POST":
            name = request.POST.get('name')
            region.name = name
            region.save()
            render(request, 'uktio/region.html')
    except Region.DoesNotExist:
        HttpResponseNotFound("<h2>Not found id</h2>")

def add_region(request:HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        region = Region(name=name)
        region.save()
        return render(request, "uktio/region.html")
    return HttpResponseNotFound("<h2>Does not found name</h2>")

def delete_region(request:HttpRequest, id:int):
    try:
        region = Region.objects.get(id=id)
        region.delete()
        return render(request, 'uktio/region.html')
    except Region.DoesNotExist:
        return HttpResponseNotFound('<h2>Region not found</h2>')

def clear_session(request:HttpRequest):
    request.session.clear()
    request.session.modified = True
    return render(request, "uktio/index.html")
