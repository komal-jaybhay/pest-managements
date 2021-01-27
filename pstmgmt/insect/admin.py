from django.contrib import admin
from .models import Insect, InsectAdvisory

# Register your models here.
class InsectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

    # def get_desc(self, instance):
    #     return instance.description
    #
    # get_desc.short_description = 'Description'


class InsectAdvisoryAdmin(admin.ModelAdmin):
    list_display = ['insect_name', 'advisory', 'suggestion']
    # def get_desc(self, instance):
    #     return instance.desc
    # get_desc.short_description = 'Description'


admin.site.register(Insect, InsectAdmin)
admin.site.register(InsectAdvisory, InsectAdvisoryAdmin)
