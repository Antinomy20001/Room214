from django.contrib import admin
from access_control.models import AccessRecord

@admin.register(AccessRecord)
class AccessRecordAdmin(admin.ModelAdmin):
    list_play = ('timestamp','label','distance','location',)
    list_filter = ('timestamp', 'location','label')
    search_fields = ('timestamp', 'location','label')