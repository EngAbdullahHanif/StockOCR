from django.contrib import admin

# Register your models here.
from .models import Item, Device, Project, ItemType, Item

class MacAddressAdmin(admin.ModelAdmin):

    search_fields = ('pk', 'mac', )


class ProjectAdmin(admin.ModelAdmin):

    search_fields = ('project_name', )


# admin.site.register(Item)
admin.site.register(Device, MacAddressAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ItemType)
admin.site.register(Item)