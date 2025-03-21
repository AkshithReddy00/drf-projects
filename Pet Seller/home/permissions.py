from rest_framework import permissions

class IsPetOwnerPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # Ensure user is authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Ensure user is the owner of the animal
        return obj.animal_owner == request.user
