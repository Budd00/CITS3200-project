from django.contrib import admin
from .models import member_info, member_details
# Register your models here.
admin.site.register(member_info)
admin.site.register(member_details)