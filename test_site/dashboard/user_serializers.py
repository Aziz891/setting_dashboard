
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import Settings_Details, Settings_Parameters


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name')


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')

        
class parameter_serializer(serializers.ModelSerializer):


    class Meta:
        model = Settings_Parameters
        fields = '__all__'

class setting_serializer(serializers.ModelSerializer):
    param  = parameter_serializer(many=True)


    class Meta:
        model = Settings_Details
        fields = [ 'id', 'substation', 'manufacturer', 'bay_number', 'creation_date', 'created_by', 'area', 'param']
    creation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_by = serializers.SerializerMethodField()


    def get_created_by(self, obj):
        # return obj.created_by_id.username if obj.created_by else None
        try:
            temp = obj.created_by.username
        except AttributeError:
            temp = None
        
        return temp
    
    def create(self, validated_data):
        param_data = validated_data.pop('param')
        setting = Settings_Details.objects.create(**validated_data, created_by = User.objects.get(pk=1))
        # setting.created_by = User.objects.get(pk=1)
        
        for param in param_data:
            Settings_Parameters.objects.create(setting_id=setting, **param)
        return setting
class setting_serializer2(serializers.ModelSerializer):


    class Meta:
        model = Settings_Details
        fields = [ 'id', 'substation', 'manufacturer', 'bay_number', 'creation_date', 'created_by', 'area']
        
    creation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    created_by = serializers.SerializerMethodField()


    def get_created_by(self, obj):
        # return obj.created_by_id.username if obj.created_by else None
        try:
            temp = obj.created_by.username
        except AttributeError:
            temp = None
        
        return temp
    
    def create(self, validated_data):
        param_data = validated_data.pop('param')
        setting = Settings_Details.objects.create(**validated_data, created_by = User.objects.get(pk=1))
        # setting.created_by = User.objects.get(pk=1)
        
        for param in param_data:
            Settings_Parameters.objects.create(setting_id=setting, **param)
        return setting

