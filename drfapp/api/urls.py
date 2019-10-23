from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

app_name = 'api'

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='jwt-token'),
    path('auth/groups/', views.GroupsView.as_view(), name='groups'),

    path('users/', views.UserListView.as_view(), name='users'),
    path('users/<int:pk>/', views.UserView.as_view(), name='users'),
]
