from django.urls import path
from . import views
from . import api


urlpatterns = [
    path('', views.api),
    path('evi-map/', views.get_evi_map),
    path('evi-pie-chart/', views.get_pie_evi),
    path('evi-line-chart/', views.get_line_evi),
    path('download-evi-map/', views.get_download_evi_map),
    path('landcover-map/', views.get_landcover_map), 
    path('download-landcover-map/', views.get_download_landcover_map),
    path('landcover-stats/', views.get_landcover_stats),
    path('mmr/', api.api_myanmar)
]
