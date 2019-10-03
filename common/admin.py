from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from common.models import AppUser, Team

base_readonly_fields = ('id', 'created_at', 'updated_at',)

class TeamMembershipInline(admin.TabularInline):
    model = Team.users.through

class AppUserAdmin(admin.ModelAdmin):
    list_display    = ('id', 'provider_id',)
    search_fields   = ('id', 'provider_id',)
    inlines         = [
        TeamMembershipInline,
    ]
    readonly_fields = base_readonly_fields
admin.site.register(AppUser, AppUserAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display        = ('__str__',)
    search_fields       = ('id', 'name',)
    filter_horizontal   = ('users',)
    readonly_fields     = base_readonly_fields
admin.site.register(Team, TeamAdmin)
