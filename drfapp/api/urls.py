from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

app_name = 'api'

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='jwt-token'),
    path('auth/groups/', views.GroupsView.as_view(), name='groups'),

    path('users/', views.UserListView.as_view(), name='users'),
    path('users/<int:pk>/', views.UserView.as_view(), name='users'),

    path('organizations/<int:pk>/', views.OrganizationView.as_view(),
         name='organizations'),
    path('organizations/<int:pk>/users/',
         views.OrganizationUserListView.as_view(), name='organization-users'),
    path('organizations/<int:pk>/users/<int:user_id>',
         views.OrganizationUserView.as_view(), name='organization-users'),
]
