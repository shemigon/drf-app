from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = 'name',


class GroupsView(ListAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
