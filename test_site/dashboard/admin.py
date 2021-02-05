from django.contrib import admin

# Register your models here.

from dashboard.models import Settings_Parameters, Settings_Details

admin.site.register(Settings_Details)
admin.site.register(Settings_Parameters)