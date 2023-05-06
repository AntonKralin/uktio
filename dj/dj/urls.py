"""
URL configuration for dj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from uktio import views

urlpatterns = [
    path('', views.main),
    path('main', views.main, name='main'),
    path('index', views.index, name="index"),
    path('about', views.about, name='about'),
    path('region/<int:id>', views.region, name='edit_region'),
    path('region', views.region, name='region'),
    path('save_region', views.save_region, name='save_region'),
    path('delete_region/<int:id>', views.delete_region, name="delete_region"),
    path('organization/<int:id>', views.organization, name='edit_organization'),
    path('organization', views.organization, name='organization'),
    path('save_organization', views.save_organization, name='save_organization'),
    path('delete_organization/<int:id>', views.delete_organization, name='delete_organization'),
    path('workers/<int:id>', views.workers, name='edit_workers'),
    path('workers', views.workers, name='workers'),
    path('save_worker', views.save_worker, name='save_worker'),
    path('delete_worker/<int:id>',views.delete_worker, name='delete_worker'),
    path('clear_session', views.clear_session, name='clear_session'),
    path('adminis/', admin.site.urls),
]
