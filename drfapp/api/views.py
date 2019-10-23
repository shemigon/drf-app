from django.contrib.auth.models import Group
from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from drfapp.api.serializers import GroupSerializer, UserOrganizationSerializer, \
    UserSerializer
from drfapp.core.models import GroupName, User


class GroupsView(ListAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


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


class UserListView(ListCreateAPIView):
    permission_classes = UserPermission,
    serializer_class = UserOrganizationSerializer

    search_fields = 'name', 'email'
    filter_fields = 'phone',

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserOrganizationSerializer
        return UserSerializer

    def get_queryset(self):
        qs = User.objects.all()
        user = self.request.user
        if user.is_superuser:
            return qs
        if user.group not in [GroupName.Administrator, GroupName.Viewer]:
            return User.objects.none()
        qs = qs.filter(organization=self.request.user.organization)
        for field in self.search_fields:
            try:
                qs = qs.filter(**{
                    f'{field}__icontains': self.request.query_params[field]
                })
            except KeyError:
                pass
        for field in self.filter_fields:
            try:
                qs = qs.filter(**{
                    f'{field}': self.request.query_params[field]
                })
            except KeyError:
                pass
        return qs

    def perform_create(self, serializer):
        self.check_object_permissions(self.request,
                                      User(**serializer.validated_data))
        return super().perform_create(serializer)


class UserView(RetrieveUpdateDestroyAPIView):
    permission_classes = UserPermission,
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserOrganizationSerializer
        return UserSerializer
