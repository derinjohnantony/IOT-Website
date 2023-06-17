from django.contrib import admin
from .models import groupdatainfo, appliancesdatainfo

# Register your models here.
admin.site.register(groupdatainfo)
admin.site.register(appliancesdatainfo)