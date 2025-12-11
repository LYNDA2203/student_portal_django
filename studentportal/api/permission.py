from rest_framework.permissions import BasePermission

class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user,'userprofile') and request.user.userprofile.role == "mentor"

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user,'userprofile') and request.user.userprofile.role == "student"

class MarkPermissions(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        # Students → only GET allowed
        if user.userprofile.role == "student":
            return request.method in ("GET", "HEAD", "OPTIONS")

        # Mentors → full access
        if user.userprofile.role == "mentor":
            return True

        return False