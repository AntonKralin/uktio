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
        select_organization = [(None, "")] + select_organization
        organization_form.fields["region"].choices = select_region
        organization_form.fields["subordinate"].choices = select_organization
        
        if id != '':
            try:
                edit_org = Organization.objects.get(id=id)
                organization_form.fields["id"].initial = id
                organization_form.fields["name"].initial = edit_org.name
                organization_form.fields["city"].initial = edit_org.city
                organization_form.fields["address"].initial = edit_org.address
                organization_form.fields["telefone"].initial = edit_org.telephone
                organization_form.initial["region"] = edit_org.region.id
                if edit_org.subordinate:
                    organization_form.initial["subordinate"] = edit_org.subordinate.id
            except Organization.DoesNotExist:
                return HttpResponseNotFound("<h1>Wrong organization<h1>")
        
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
        
        if id_org == '':
            organization = Organization(name=name, city=city, 
                                    address=address, telephone=telephone,
                                    region=region, subordinate=sub_org)
        else:
            organization = Organization.objects.get(id=id_org)
            organization.name = name
            organization.city = city
            organization.address = address
            organization.telephone = telephone
            organization.region = region
            organization.subordinate=sub_org
        organization.save()
        
        user_id = request.session.get('user', None)
        user = Users.objects.get(id=user_id)
        user.organization.add(organization)
        user.save
        
    return HttpResponsePermanentRedirect("/organization")

def delete_organization(request:HttpRequest, id:int):
    try:
        buf_org = Organization.objects.get(id=id)
        buf_org.delete()
        return HttpResponsePermanentRedirect("/organization")
    except Organization.DoesNotExist:
        return HttpResponseNotFound('<h1>Organization not found</h1>')
    return HttpResponsePermanentRedirect("/organization")

def workers(request:HttpRequest, id=''):
    id_user = request.session.get('user', None)
    if id_user:
        user = Users.objects.get(id=id_user)
        query_orgs = user.organization.all()
        orgs = organization_query_to_select(query_orgs)
        workers_form = WorkerForm()
        workers_form.fields["organization"].choices = orgs
        
        #workers = Workers.objects.all()
        workers = Workers.objects.filter(organization__in=user.organization.all())
        
        if id != '':
            worker = Workers.objects.get(id=id)
            workers_form.fields["id"].initial = worker.id
            workers_form.fields["name"].initial = worker.name
            workers_form.fields["surname"].initial = worker.surname
            workers_form.fields["job"].initial = worker.job
            workers_form.initial["organization"] =worker.organization.id
        
        context = {"worker_form": workers_form,
                   "workers": workers}
        return render(request, 'uktio/workers.html', context=context)
    return HttpResponseNotFound("<h1>please logon</h1>")

def save_worker(request:HttpRequest):
    if request.method == 'POST':
        id_worker = request.POST.get('id', None)
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        job = request.POST.get("job")
        id_org = request.POST.get("organization")
        org = Organization.objects.get(id=id_org)
        
        if not id_worker:
            worker = Workers(name=name, surname=surname, job=job, organization=org)
        else:
            worker = Workers.objects.get(id=id_worker)
            worker.name = name
            worker.surname = surname
            worker.job = job
            worker.organization = org
            
        worker.save()
        
    return HttpResponsePermanentRedirect('/workers')

def delete_worker(request:HttpRequest, id=None):
    if id:
        worker = Workers.objects.get(id=id)
        worker.delete()
        return HttpResponsePermanentRedirect("/workers")
    return HttpResponsePermanentRedirect("<h1>worker not foutd</h1>")

def cabinets(request:HttpRequest, id=""):
    id_user = request.session.get('user', None)
    if id_user:
        user = Users.objects.get(id=id_user)
        query_org = user.organization.all()
        org = organization_query_to_select(query_org)
        cabinet_form = CabinetForm()
        cabinet_form.fields["organization"].choices = org
        
        if id != "":
            cabinet = Cabinet.objects.get(id=id)
            cabinet_form.fields['name'].initial = cabinet.name
            cabinet_form.fields['description'].initial = cabinet.description
            cabinet_form.initial['organization'] = cabinet.organization.id
            cabinet_form.fields['id'].initial = cabinet.id
        
        cabinets = Cabinet.objects.filter(organization__in=user.organization.all())
        
        context = {"cabinet_form": cabinet_form,
                   "cabinets": cabinets}
        return render(request, 'uktio/cabinets.html', context=context)
    return HttpResponseNotFound("<h1>Please logon</h1>")

def save_cabinet(request:HttpRequest):
    if request.method == "POST":
        id_cabinet = request.POST.get('id', None)
        name = request.POST.get('name')
        description = request.POST.get('description')
        org_id = request.POST.get('organization')
        org = Organization.objects.get(id=org_id)
        
        if id_cabinet:
            cabinet = Cabinet.objects.get(id=id_cabinet)
            cabinet.name = name
            cabinet.description = description
            cabinet.organization = org
        else:
            cabinet = Cabinet(name=name, description=description, organization=org)
        cabinet.save()
        return HttpResponsePermanentRedirect('/cabinets')
    return HttpResponseNotFound("<h1>Not found post</h1>")

def delete_cabinet(request:HttpRequest, id=None):
    if id:
        cabinet = Cabinet.objects.get(id=id)
        cabinet.delete()
        return HttpResponsePermanentRedirect('/cabinets')
    return HttpResponseNotFound('<h1>id not found</h1')

def clear_session(request:HttpRequest):
    request.session.clear()
    request.session.modified = True
    return render(request, "uktio/index.html")
