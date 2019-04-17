from django.contrib import admin
from .models import User, Sponsorship, Request, Complain

admin.site.register(User)
admin.site.register(Sponsorship)
admin.site.register(Request)
admin.site.register(Complain)