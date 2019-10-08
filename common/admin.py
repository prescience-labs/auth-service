from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _

from .models import Team, User

base_readonly_fields = ('id', 'created_at', 'updated_at',)

class TeamMembershipInline(admin.TabularInline):
    model = Team.users.through

class TeamAdmin(admin.ModelAdmin):
    list_display        = ('__str__',)
    search_fields       = ('id', 'name',)
    filter_horizontal   = ('users',)
    readonly_fields     = base_readonly_fields
admin.site.register(Team, TeamAdmin)

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'token_valid_timestamp')}),
        (_('Password reset'), {'fields': ('password_reset_token', 'password_reset_expiration')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    inlines         = [
        TeamMembershipInline,
    ]
admin.site.register(User, CustomUserAdmin)
