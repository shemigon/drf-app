from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from drfapp.core.models import GroupName, User


class UserPermission(IsAuthenticated):
    """
    Administrator: Full access to CRUD Any User in his org and RU Organization
    Viewer: List and Retrieve any User in his org.
    User: CRU his own user
    """

    def has_permission(self, request, view):
        def f():
            user = request.user
            group = user.group
            if request.method == 'POST' and group != GroupName.Administrator:
                return False
            return True

        return super().has_permission(request, view) and f()

    def has_object_permission(self, request, view, obj: User):
        user = request.user
        group = user.group
        if user.organization_id != obj.organization_id:
            return False
        if group == GroupName.Administrator:
            if request.method == 'DELETE' and user == obj:
                return False  # don't delete yourself
            return True
        if request.method == 'DELETE':
            return False
        if user == obj:
            return True
        if group == GroupName.Viewer and request.method == 'GET':
            return True
        return False


class OrganizationPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if view.kwargs.get('pk', '') != request.user.organization_id:
            return False

        allowed_groups = [GroupName.Administrator]
        if request.method in SAFE_METHODS:
            allowed_groups.append(GroupName.Viewer)
        return request.user.group in allowed_groups
