from django.views import View
from django.http import HttpResponse, JsonResponse
from datetime import date, timedelta
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from  django.core.files.uploadhandler import FileUploadHandler
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from .xml_parse import setting_check
from rest_framework import permissions



class Setting_File_Handler(FileUploadHandler):

    def receive_data_chunk(self,raw_data, start):
        print('fdfdf')
        pass
    def file_complete(self, file_size):
        print('fdfdf')
        pass



class Setting_Check(APIView):
     parser_classes = (MultiPartParser, FormParser, JSONParser)
     permission_classes = (permissions.AllowAny,)
  
   
     def post(self, request, *args, **kwargs):
         

        
        setting_file = request.FILES['file'].read()
        json_setting = setting_check(setting_file)
        response = JsonResponse({'result': json_setting})
      
        
        return response

