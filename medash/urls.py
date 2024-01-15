from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("medash/admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('medash/', include('main.urls')),
]
