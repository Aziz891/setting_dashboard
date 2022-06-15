
from django.urls import path
from .views import current_user, UserList, Setting_Details_viewset, Setting_Details_viewset2,  settings_chart, settings_chart2, settings_export, rpi_api_scan, rpi_api_get_settings, area_chart, Substations_viewset, Setting_Proper_viewset2, settings_relay, Setting_Details_viewset3, rpi_api_get_faults, rpi_api_get_fault, rpi_api_get_file, rpi_api_get_file2
from dashboard.setting_check import Setting_Check
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import obtain_jwt_token




app_name= 'dashboard'

urlpatterns = [


  path('setting_check/', csrf_exempt(Setting_Check.as_view()) , name='setting_check'),
  path('token-auth/', obtain_jwt_token),
  path('current_user/', current_user),
  path('users/', UserList.as_view())  ,
  path('chart/', settings_chart.as_view()),  
  path('chart2/', settings_chart2.as_view())  ,
  path('chart3/', area_chart.as_view())  ,
  path('export/', settings_export.as_view())  ,
  path('rpi/', rpi_api_scan.as_view())  ,
  path('rpi_set/', rpi_api_get_settings.as_view())  ,
  path('rpi_fault/', rpi_api_get_faults.as_view())  ,
  path('rpi_fault2/', rpi_api_get_fault.as_view())  ,
  path('rpi_file/', rpi_api_get_file.as_view())  ,
  path('rpi_file2/', rpi_api_get_file2.as_view())  ,
  path('relay_set/', settings_relay.as_view())  ,
  path('list/', Setting_Details_viewset3.as_view({'get' : 'list'}))  








]


from .views import Setting_Details_viewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'setting', Setting_Proper_viewset2, basename='user')
router.register(r'subs', Substations_viewset, basename='user2')
router.register(r'collected', Setting_Details_viewset2, basename='user3')
urlpatterns += router.urls


