from django.contrib.auth.models import Group
from rest_framework import serializers

from drfapp.core.models import Organization, User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = 'name',


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = 'id', 'name', 'phone', 'address'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'name', 'phone', 'email', 'organization', 'birthdate'


class UserOrganizationSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = User
        fields = 'id', 'name', 'phone', 'email', 'organization', 'birthdate'
