from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from common.models import AppUser, Team

class AppUserAdmin(admin.ModelAdmin):
    list_display    = ('id', 'provider_id',)
    search_fields   = ('id', 'provider_id',)
    readonly_fields = ('id', 'provider_id',)
admin.site.register(AppUser, AppUserAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display        = ('__str__',)
    search_fields       = ('id', 'name',)
    filter_horizontal   = ('users',)
admin.site.register(Team, TeamAdmin)
