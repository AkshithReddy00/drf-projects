from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):

    def has_permission(self, request, view):
    # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    
    def has_object_permission(self, request, view, obj):
        return obj.blog_owner == request.user