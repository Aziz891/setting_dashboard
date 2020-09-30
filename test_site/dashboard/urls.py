
from django.urls import path
from . import views
from dashboard.setting_check import Setting_Check
from django.views.decorators.csrf import csrf_exempt



app_name= 'dashboard'

urlpatterns = [


  path('setting_check/', csrf_exempt(Setting_Check.as_view()) , name='setting_check'),
 
  








]