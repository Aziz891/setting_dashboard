from django.db import models
from django.db import models
from django.contrib.auth.models import User
import datetime


class Settings_Details(models.Model):
    id= models.AutoField(primary_key=True)
    substation = models.CharField(max_length=100, blank=True, null=True)
    bay_number = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    scheme_type = models.CharField(max_length=100, blank=True, null=True)
    serial_nuber = models.CharField(max_length=100, blank=True, null=True)
    function_type = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, models.CASCADE, blank=False, null=True, related_name='setting')
    creation_date = models.DateTimeField( auto_now_add=True, auto_now=False ,blank=True, null=True)


class Settings_Parameters(models.Model):
    id= models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100, blank=True, null=True)
    Description = models.CharField(max_length=100, blank=True, null=True)
    Value = models.CharField(max_length=100, blank=True, null=True)
    Setting_Key = models.ForeignKey(Settings_Details, models.CASCADE, blank=False, null=False, related_name='detail')








# Create your models here.
