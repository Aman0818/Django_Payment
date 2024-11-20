from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from User import models

class user_registeredAdmin(ModelAdmin):
    list_display=['user_name','payment_status','registration_date']
    search_fields=['user_name','payment_status','user_email','user_phone']

admin.site.register(models.user_registered,user_registeredAdmin)
