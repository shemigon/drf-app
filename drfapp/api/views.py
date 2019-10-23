from django.contrib.auth.models import Group
from rest_framework.generics import get_object_or_404, ListAPIView, \
    ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from drfapp.api.permissions import OrganizationPermission, UserPermission
from drfapp.api.serializers import GroupSerializer, OrganizationSerializer, \
    UserMinSerializer, UserOrganizationSerializer, UserSerializer
from drfapp.core.models import GroupName, Organization, User


class GroupsView(ListAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


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


class OrganizationView(RetrieveUpdateAPIView):
    permission_classes = OrganizationPermission,
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()


class OrganizationUserListView(ListAPIView):
    permission_classes = OrganizationPermission,
    serializer_class = UserMinSerializer

    def get_queryset(self):
        return User.objects.filter(organization=self.request.user.organization)


class OrganizationUserView(RetrieveAPIView):
    permission_classes = OrganizationPermission, UserPermission
    serializer_class = UserMinSerializer

    def get_object(self):
        obj = get_object_or_404(
            User,
            organization=self.request.user.organization,
            id=self.kwargs['user_id']
        )

        self.check_object_permissions(self.request, obj)

        return obj
