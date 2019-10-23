from django.contrib import admin

from drfapp.core.models import Organization, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = 'name', 'email', 'organization', 'is_active'

    def save_model(self, request, obj: User, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        return super(UserAdmin, self).save_model(request, obj, form, change)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = 'name',
