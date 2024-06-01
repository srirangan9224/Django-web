from django.contrib import admin
from .models import *

# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    list_display = ("sender","timestamp","read","archived")
admin.site.register(User)
admin.site.register(Email,EmailAdmin)