from django.urls import path
from . import views


urlpatterns = [
    path('api/', views.api),
    path('api/evi-map/', views.get_evi_map),
    path('api/evi-pie-chart/', views.get_pie_evi),
    path('api/evi-line-chart/', views.get_line_evi),
    path('api/download-evi-map/', views.get_download_evi_map),
    path('api/landcover-map/', views.get_landcover_map), 
    path('api/download-landcover-map/', views.get_download_landcover_map),
    path('api/landcover-stats/', views.get_landcover_stats),
]
