from django.contrib import admin

class StaffOnlyAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff

admin_site = StaffOnlyAdminSite(name='staff_admin')
admin.site = admin_site
