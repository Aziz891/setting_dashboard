from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .user_serializers import UserSerializer, UserSerializerWithToken, setting_serializer
from rest_framework import viewsets
from .models import Settings_Details, Settings_Parameters
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncMonth, TruncDay
from django.db.models import Count, Q, Sum
from datetime import datetime
from django.http import HttpResponse
import csv
import pandas as pd
from io import BytesIO


class Setting_Details_viewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = setting_serializer
    queryset = Settings_Details.objects.all()

    # def list(self, request):
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = Settings_Details.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)


class settings_chart(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        data = Settings_Details.objects.annotate(x=TruncMonth(
            'creation_date')) .values('x').annotate(
            y=Count('id')).values('x', 'y')
        data = [ {'t': i["x"].strftime("%Y-%m-%d"), 'y': i['y'] } for i in data ]

        return Response(data)
class settings_chart2(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        data = Settings_Details.objects.values( 'manufacturer').annotate(
            y=Count('manufacturer')).exclude(manufacturer__isnull= True)
        temp = [[i['manufacturer'] for i in data ], [i['y'] for i in data ] ] 

        return Response(temp)
class settings_export(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        # data = Settings_Details.objects.get_object_or_404
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="export.csv"'
        # writer = csv.writer(response, dialect='excel')
        settings = Settings_Parameters.objects.filter(setting_id=request.query_params["id"]).values_list('name', 'value')
        pd_setting = pd.DataFrame(settings)
        with BytesIO() as b:
        # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            pd_setting.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            return HttpResponse(b.getvalue(), content_type='application/vnd.ms-excel')
       
        
        # return response

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
