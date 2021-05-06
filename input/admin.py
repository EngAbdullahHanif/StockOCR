from django.contrib import admin

# Register your models here.
from .models import Item, macItem, Project

admin.site.register(Item)
admin.site.register(macItem)
admin.site.register(Project)