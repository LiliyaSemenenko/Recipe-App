"""
Django admin customization.
"""
from django.contrib import admin
# UserAdmin: base class used for default django authentication system
# BaseUserAdmin: named like that because we don't want our UserAdmin
# and this one to conflict bcs of same names
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# integrates with django translation system
# (automatically translating the text)
# _(section_to_translate)
from django.utils.translation import gettext_lazy as _
from core import models
from core.models import UserProfile

class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'
    fk_name = 'user'
    # form = UserProfileForm


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

    ordering = ['id']  # order users by id
    list_display = ['email', 'name']  # list these items

    # ((title, {'fields': ('','')}),)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # title = None
        (_('Personal Info'), {'fields': ('name',)}),  # title = Personal Info
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    readonly_fields = ['last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # used for page look
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


admin.site.register(models.UserProfile)
# register User model and assign custom UserAdmin class
admin.site.register(models.User, UserAdmin)
# register Recipe model (no custom Django admin class)
admin.site.register(models.Recipe)
# register Tag model so that it's manageble through Django Admin Interface
admin.site.register(models.Tag)
# register Ingredient model so that it's manageble through DAI
admin.site.register(models.Ingredient)
