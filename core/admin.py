from django.contrib import admin
from core.models import User, Face, Person

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_play = ('username','email','create_time',)
    list_filter = ('username',)
    search_fields = ('username','email',)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_play = ('name','title','face')
    list_filter = ('name',)
    search_fields = ('name',)