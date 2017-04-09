from django.contrib import admin

from restapi.models import *

# Register your models here.

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Token)
