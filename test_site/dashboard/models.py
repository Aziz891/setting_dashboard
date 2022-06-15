from ipaddress import ip_address
from django.db import models
from django.db import models
from django.contrib.auth.models import User
import datetime

class Substations(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)

class Settings_Details(models.Model):
    id= models.AutoField(primary_key=True)
    bay_number = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    scheme_type = models.CharField(max_length=100, blank=True, null=True)
    serial_nuber = models.CharField(max_length=100, blank=True, null=True)
    function_type = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, models.CASCADE, db_column="created_by", blank=False, null=True,  related_name='setting')
    creation_date = models.DateTimeField( auto_now_add=True, auto_now=False ,blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    substation = models.ForeignKey(Substations, models.CASCADE, db_column="substation", blank=False, null=True,  related_name='relay')
    
class Fault(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    trigger_date = models.DateTimeField( auto_now_add=True, auto_now=False ,blank=True, null=True)
    cfg = models.FileField(max_length=1000, blank=True, null=True, upload_to='faults')
    dat = models.FileField(max_length=1000, blank=True, null=True, upload_to='faults')
    relay = models.ForeignKey(Settings_Details, models.CASCADE, db_column="relay", blank=False, null=True,  related_name='fault')

class Settings_Proper(models.Model):
    id= models.AutoField(primary_key=True)
    creation_date = models.DateTimeField( auto_now_add=True, auto_now=False ,blank=True, null=True)
    relay = models.ForeignKey(Settings_Details, models.CASCADE, db_column="relay", blank=False, null=True,  related_name='proper')
    

class Settings_Parameters(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    setting_id = models.ForeignKey(Settings_Proper, models.CASCADE, db_column="settings_id", blank=True, null=True, related_name='param')











# Create your models here.
