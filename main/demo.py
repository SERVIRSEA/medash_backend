import json
import orjson
from collections import defaultdict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.models import *
from main.serializers import (
    LandCoverNationalSerializer,
    LandCoverProvinceSerializer,
    LandCoverDistrictSerializer,
    LandCoverProtectedAreaSerializer,
    ForestCoverNationalSerializer,
    ForestCoverProvinceSerializer,
    ForestCoverDistrictSerializer,
    ForestCoverProtectedAreaSerializer,
    SARAlertNationalSerializer,
    SARAlertProvinceSerializer,
    SARAlertDistrictSerializer,
    SARAlertProtectedAreaSerializer,
    GLADAlertNationalSerializer,
    GLADAlertProvinceSerializer,
    GLADAlertDistrictSerializer,
    GLADAlertProtectedAreaSerializer,
    FireHotspotNationalSerializer,
    FireHotspotProvinceSerializer,
    FireHotspotDistrictSerializer,
    FireHotspotProtectedAreaSerializer
)
from django.conf import settings


# STW_FORECAST_PRECIPITATION = settings.STW_FORECAST_PRECIPITATION
# STW_FORECAST_TEMPERATURE = settings.STW_FORECAST_TEMPERATURE
# STW_PAST_PRECIPITATION = settings.STW_PAST_PRECIPITATION
# STW_PAST_TEMPERATURE = settings.STW_PAST_TEMPERATURE
# SEASONAL_PRECIPITATION = settings.SEASONAL_PRECIPITATION
# SEASONAL_TEMPERATURE = settings.SEASONAL_TEMPERATURE


# def get_weather_map(weather_param="precipitation", weather_type="past", download="False"):
#         CAMBODIA_COUNTRY_BOUNDARY  = "projects/servir-mekong/Cambodia-Dashboard-tool/boundaries/cambodia_country"
#         geometry = ee.FeatureCollection(CAMBODIA_COUNTRY_BOUNDARY)
#         if weather_type=="forecast":
#             if weather_param == "precipitation":
#                 image_collection = ee.ImageCollection(STW_FORECAST_PRECIPITATION)
#             else:
#                 image_collection = ee.ImageCollection(STW_FORECAST_TEMPERATURE)
        
#         elif weather_type=="past":
#             if weather_param == "precipitation":
#                 image_collection = ee.ImageCollection(STW_PAST_PRECIPITATION)
#             else:
#                 image_collection = ee.ImageCollection(STW_PAST_TEMPERATURE)
        
#         elif weather_type == "seasonal":
#             if weather_param == "precipitation":
#                 image_collection =  ee.ImageCollection(SEASONAL_PRECIPITATION)
#             else:
#                 image_collection =  ee.ImageCollection(SEASONAL_TEMPERATURE)     

#         # Sort the collection by date in descending order
#         sorted_collection = image_collection.sort('system:time_start', False)

#         # Get the first (latest) image from the sorted collection
#         latest_image = sorted_collection.first().clip(geometry)
#         image = latest_image.selfMask()
#         imgScale = image.projection().nominalScale()
#         image = image.reproject(crs='EPSG:4326', scale=imgScale)
        
#         # Rename the band if needed
#         image = image.rename([weather_param])
#         # Compute minimum and maximum values
#         stats = image.reduceRegion(reducer=ee.Reducer.minMax(), geometry=geometry, scale=imgScale)
#         min_value = stats.get(weather_param+'_min')
#         max_value = stats.get(weather_param+'_max')

#         # Round the min and max values to 2 decimal places
#         min_value_rounded = round(min_value.getInfo(), 2)
#         max_value_rounded = round(max_value.getInfo(), 2)

#         # Print the rounded values
#         print("Min:", min_value_rounded, "Max:", max_value_rounded)
#         return stats

# get_weather_map("temperature", "past") 


def get_report_stat(report_type, start_year, end_year):
    area_type = "province"
    area_id = 21
    try:
        if report_type == "forest-monitoring":
            area_type_mapping = {
                'country': {'model': ForestCoverNational, 'serializer': ForestCoverNationalSerializer, 'field_name': 'country'},
                'province': {'model': ForestCoverProvince, 'serializer': ForestCoverProvinceSerializer, 'field_name': 'gid'},
                'district': {'model': ForestCoverDistrict, 'serializer': ForestCoverDistrictSerializer, 'field_name': 'dist_code'},
                'protected_area': {'model': ForestCoverProtectedArea, 'serializer': ForestCoverProtectedAreaSerializer, 'field_name': 'pid'},
            }
        else:
            raise ValueError("Invalid report type")

        area_info = area_type_mapping.get(area_type)
        if area_info is None:
            raise ValueError(f"Invalid area type: {area_type}")

        db_model = area_info['model']
        
        if db_model:
            if area_type == 'country':
                start_year_data = db_model.objects.filter(year=int(start_year))
                end_year_data = db_model.objects.filter(year=int(end_year))
            else:
                field_name = area_info['field_name']
                start_year_data = db_model.objects.filter(**{field_name: area_id}, year=int(start_year))
                end_year_data = db_model.objects.filter(**{field_name: area_id}, year=int(end_year))
                
            # Serialize data using the appropriate serializer for both start and end years
            serializer_class = area_info['serializer']
            start_year_serializer = serializer_class(start_year_data, many=True)
            end_year_serializer = serializer_class(end_year_data, many=True)
            
            # Extract the 'areaHa' value for the specified year
            start_areaHa_value = None
            end_areaHa_value = None
            for entry in start_year_serializer.data:
                if 'forest_areaHa' in entry:
                    start_areaHa_value = float(entry['forest_areaHa'])
                    break
            
            for entry in end_year_serializer.data:
                if 'forest_areaHa' in entry:
                    end_areaHa_value = float(entry['forest_areaHa'])
                    break
            
            print("Start year areaHa:", start_areaHa_value)
            print("End year areaHa:", end_areaHa_value)
    except Exception as e:
        transformed_data = {'error': str(e)}
        print("Exception:", e)

get_report_stat("forest-monitoring", 2010, 2022)

# python manage.py shell < ./main/demo.py