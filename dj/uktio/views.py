from django.shortcuts import render
from django.http import HttpRequest, HttpResponseNotFound, HttpResponsePermanentRedirect
from .models import *
from .forms import *
from .functions import *


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

def region(request:HttpRequest, id=""):
    user_id = request.session.get('user', None)
    if user_id:
        region_form = RegionForm()
        if id != "":
            edit_region = Region.objects.get(id=id)
            region_form = RegionForm(initial={"id":edit_region.id, 'name':edit_region.name})
            
        user = Users.objects.get(id=user_id)
        regions = user.region.all()
        context = {'region_form': region_form,
                   'regions': regions}
        return render(request, 'uktio/region.html', context=context)
    return HttpResponseNotFound('<h1>No user</h1>')

def save_region(request:HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        id = request.POST.get("id")
        if id == "":
            region = Region(name=name)
        else:
            try:
                region = Region.objects.get(id=id)
                if request.method == "POST":
                    name = request.POST.get('name')
                    region.name = name
            except Region.DoesNotExist:
                HttpResponseNotFound("<h2>Not found id</h2>")
        
        region.save()
        id_user = request.session.get('user')
        user = Users.objects.get(id=id_user)
        user.region.add(region)
        return HttpResponsePermanentRedirect("/region")
    return HttpResponseNotFound("<h2>Does not found name</h2>")

def delete_region(request:HttpRequest, id:int):
    try:
        region = Region.objects.get(id=id)
        region.delete()
        return HttpResponsePermanentRedirect('/region')
    except Region.DoesNotExist:
        return HttpResponseNotFound('<h2>Region not found</h2>')

def organization(request:HttpRequest, id=''):
    user_id = request.session.get('user', None)
    if user_id:
        user = Users.objects.get(id=user_id)
        
        organization_form = OrganizationForm() 
        query_regions = user.region.all()
        query_organization = user.organization.all()
        select_region = region_query_to_select(query_regions)
        select_organization = organization_query_to_select(query_organization)
        organization_form.fields["region"].choices = select_region
        organization_form.fields["subordinate"].choices = select_organization
        
        org_list = user.organization.all()
        
        context = {"organization_form": organization_form,
                   "organizations": org_list}
        return render(request, "uktio/organization.html", context)
    return HttpResponseNotFound("<h1>Not logon</h1>")

def save_organization(request:HttpRequest):
    if request.method == "POST":
        id_org = request.POST.get("id", '')
        name = request.POST.get("name", '')
        city = request.POST.get("city", '')
        address = request.POST.get("address", '')
        telephone = request.POST.get("telefone", '')
        id_region = request.POST.get("region", None)
        id_subordinate = request.POST.get("subordinate", None)
        
        region = None
        if id_region:
            region = Region.objects.get(id=id_region)
            
        sub_org = None
        if id_subordinate:
            sub_org = Organization.objects.get(id=id_subordinate)
        
        organization = Organization(name=name, city=city, 
                                    address=address, telephone= telephone,
                                    region=region, subordinate=sub_org)
        organization.save()
        
        user_id = request.session.get('user', None)
        user = Users.objects.get(id=user_id)
        user.organization.add(organization)
        user.save
        
    return HttpResponsePermanentRedirect("/organization")

def clear_session(request:HttpRequest):
    request.session.clear()
    request.session.modified = True
    return render(request, "uktio/index.html")
