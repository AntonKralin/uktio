from django.db import models

# Create your models here.
class Users(models.Model):
    login = models.CharField(max_length=100, unique=True, blank=False,
                             verbose_name="Login", help_text="Enter login")
    password = models.CharField(max_length=200, blank=False,
                                verbose_name="Password",
                                help_text="Enter password")
    last_logon = models.DateTimeField(blank=True, null=True,
                                      verbose_name="DateTime last logon",
                                      help_text="Enter DateTime last logon")
    last_wrong_logon = models.DateTimeField(blank=True, null=True,
                                            verbose_name="DateTime last bad logon",
                                            help_text="Enter DateTime last bad logon")
    is_superuser = models.BooleanField(default=False,
                                      verbose_name="Is user Superadmin",
                                      help_text="True - Superuser, defaulf=False")
    is_view = models.BooleanField(default=True,
                                  verbose_name="Is user only view",
                                  help_text='True - only view, default=True')
    region = models.ManyToManyField('Region', help_text="Regions")
    organization = models.ManyToManyField('Organization', help_text="Organization")
    
    objects = models.Manager()
    
    
class Region(models.Model):
    name = models.CharField(max_length=200, unique=False,
                            verbose_name="Name of Region",
                            help_text="Enter name of Region")
    
    objects = models.Manager()
  
  
class Organization(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=False,
                            verbose_name="Name", help_text="Enter name")  
    city = models.CharField(max_length=100, blank=False, unique=False,
                            verbose_name="City", help_text="Enter city")
    address = models.CharField(max_length=200, blank=False, unique=False, 
                               verbose_name="address", help_text="Enter address")
    telephone = models.CharField(max_length=20, blank=True, unique=False,
                                 verbose_name="telephone", help_text="Enter telephone number")
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    subordinate = models.ForeignKey("self", on_delete=models.SET_NULL, 
                                       blank=True, null=True)

    objects = models.Manager()


class Workers(models.Model):
    surname = models.CharField(max_length=100, blank=False, unique=False,
                               verbose_name="Surname", help_text="Enter surname")
    name = models.CharField(max_length=100, blank=False, unique=False,
                            verbose_name="Name", help_text="Enter name")
    job = models.CharField(max_length=200, blank=True, default=None,
                           verbose_name="Job", help_text="Enter job")
    id_organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    objects = models.Manager()
    

class Cabinet(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=False,
                            verbose_name='Name', help_text="Enter name")
    description = models.CharField(max_length=200, blank=True, null=True, 
                                   verbose_name='Description',
                                   help_text='Enter description')
    id_organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    objects = models.Manager()
    