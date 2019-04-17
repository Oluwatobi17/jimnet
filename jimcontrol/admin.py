from django.contrib import admin
from .models import AdminUser, Staff, Registrationcode

admin.site.register(AdminUser)
admin.site.register(Staff)
admin.site.register(Registrationcode)