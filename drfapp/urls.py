from django.contrib import admin
from django.urls import include, path

from drfapp.core.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('drfapp.api.urls')),
    path('api/web/', include('rest_framework.urls')),

    path('', HomeView.as_view()),
]
