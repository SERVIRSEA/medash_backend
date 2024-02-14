import json
import orjson
from collections import defaultdict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import (
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

class DBData:

    def __init__(self, area_type, area_id):
        self.area_type = area_type
        if area_type == "district":
            self.area_id = int(area_id)
        else:
            self.area_id = area_id

    def get_landcover_stat(self, start_year, end_year, landcover_type='all'):
        try:
            # Use a dictionary to map area types to model classes and serializers
            area_type_mapping = {
                'country': {'model': LandCoverNational, 'serializer': LandCoverNationalSerializer, 'field_name': 'country'},
                'province': {'model': LandCoverProvince, 'serializer': LandCoverProvinceSerializer, 'field_name': 'gid'},
                'district': {'model': LandCoverDistrict, 'serializer': LandCoverDistrictSerializer, 'field_name': 'dist_code'},
                'protected_area': {'model': LandCoverProtectedArea, 'serializer': LandCoverProtectedAreaSerializer, 'field_name': 'pid'},
            }

            # Retrieve the corresponding model class and serializer based on area type
            area_info = area_type_mapping.get(self.area_type)
            if area_info is None:
                raise ValueError(f"Invalid area type: {self.area_type}")

            # Filter data based on the chosen model and area_id
            db_model = area_info['model']
            if db_model:
                query_params = {
                    'year__range': (int(start_year), int(end_year)),
                }

                if landcover_type != 'all':
                    query_params['landcover'] = landcover_type

                if self.area_type == 'country':
                    db_data = db_model.objects.filter(**query_params)
                else:
                    field_name = area_info['field_name']
                    dist_code = self.area_id
                    query_params[field_name] = dist_code
                    db_data = db_model.objects.filter(**query_params)
                    
                
                # Serialize data using the appropriate serializer
                serializer_class = area_info['serializer']
                serializer = serializer_class(db_data, many=True)
                serialized_data = serializer.data

                # Organize data into the desired format
                if landcover_type == 'all':
                    result_data = defaultdict(dict)

                    for entry in serialized_data:
                        year = str(entry['year'])
                        result_data[year][entry['landcover']] = float(entry['areaHa'])
                else:
                    result_data = defaultdict(float)

                    for entry in serialized_data:
                        year = str(entry['year'])
                        result_data[year] += float(entry['areaHa'])

                # Convert to a regular dictionary
                result_dict = dict(result_data)

                # Optionally, convert to JSON using orjson
                data = orjson.dumps(result_dict) # option=orjson.OPT_INDENT_2
                # print(data)
            else:
                data = {'error': f"No model defined for area type: {self.area_type}"}

        except Exception as e:
            data = {'error': str(e)}

        return data

    def get_forest_monitoring_stat(self, start_year, end_year):
        try:
            # Use a dictionary to map area types to model classes and serializers
            area_type_mapping = {
                'country': {'model': ForestCoverNational, 'serializer': ForestCoverNationalSerializer, 'field_name': 'country'},
                'province': {'model': ForestCoverProvince, 'serializer': ForestCoverProvinceSerializer, 'field_name': 'gid'},
                'district': {'model': ForestCoverDistrict, 'serializer': ForestCoverDistrictSerializer, 'field_name': 'dist_code'},
                'protected_area': {'model': ForestCoverProtectedArea, 'serializer': ForestCoverProtectedAreaSerializer, 'field_name': 'pid'},
            }

            # Retrieve the corresponding model class and serializer based on area type
            area_info = area_type_mapping.get(self.area_type)
            if area_info is None:
                raise ValueError(f"Invalid area type: {self.area_type}")

            # Filter data based on the chosen model and area_id
            db_model = area_info['model']
            if db_model:
                if self.area_type == 'country':
                    db_data = db_model.objects.filter(
                        year__range=(int(start_year), int(end_year))
                    )
                else:
                    field_name = area_info['field_name']
                    db_data = db_model.objects.filter(
                        **{field_name: self.area_id},
                        year__range=(int(start_year), int(end_year))
                    )

                # Serialize data using the appropriate serializer
                serializer_class = area_info['serializer']
                serializer = serializer_class(db_data, many=True)
                data = serializer.data
                formatted_data = {str(entry['year']): {"forest": float(entry['forest_areaHa']), "noneForest": float(entry['nonforest_areaHa'])} for entry in data}
            else:
                formatted_data = {'error': f"No model defined for area type: {self.area_type}"}

        except Exception as e:
            formatted_data = {'error': str(e)}

        return formatted_data

    def get_sar_alert_stat(self, start_year, end_year):
        try:
            # Use a dictionary to map area types to model classes and serializers
            area_type_mapping = {
                'country': {'model': SARAlertNational, 'serializer': SARAlertNationalSerializer, 'field_name': 'country'},
                'province': {'model': SARAlertProvince, 'serializer': SARAlertProvinceSerializer, 'field_name': 'gid'},
                'district': {'model': SARAlertDistrict, 'serializer': SARAlertDistrictSerializer, 'field_name': 'dist_code'},
                'protected_area': {'model': SARAlertProtectedArea, 'serializer': SARAlertProtectedAreaSerializer, 'field_name': 'pid'},
            }

            # Retrieve the corresponding model class and serializer based on area type
            area_info = area_type_mapping.get(self.area_type)
            if area_info is None:
                raise ValueError(f"Invalid area type: {self.area_type}")

            # Filter data based on the chosen model and area_id
            db_model = area_info['model']
            if db_model:
                if self.area_type == 'country':
                    db_data = db_model.objects.filter(
                        year__range=(int(start_year), int(end_year))
                    )
                else:
                    field_name = area_info['field_name']
                    db_data = db_model.objects.filter(
                        **{field_name: self.area_id},
                        year__range=(int(start_year), int(end_year))
                    )

                # Serialize data using the appropriate serializer
                serializer_class = area_info['serializer']
                serializer = serializer_class(db_data, many=True)
                data = serializer.data
            # Transform the data into the desired format
                transformed_data = {str(entry['year']): float(entry['areaHa']) for entry in data}
                # print(transformed_data)
            else:
                transformed_data = {'error': f"No model defined for area type: {self.area_type}"}

        except Exception as e:
            transformed_data = {'error': str(e)}

        return transformed_data

    def get_glad_alert_stat(self, start_year, end_year):
        try:
            # Use a dictionary to map area types to model classes and serializers
            area_type_mapping = {
                'country': {'model': GLADAlertNational, 'serializer': GLADAlertNationalSerializer, 'field_name': 'country'},
                'province': {'model': GLADAlertProvince, 'serializer': GLADAlertProvinceSerializer, 'field_name': 'gid'},
                'district': {'model': GLADAlertDistrict, 'serializer': GLADAlertDistrictSerializer, 'field_name': 'dist_code'},
                'protected_area': {'model': GLADAlertProtectedArea, 'serializer': GLADAlertProtectedAreaSerializer, 'field_name': 'pid'},
            }

            # Retrieve the corresponding model class and serializer based on area type
            area_info = area_type_mapping.get(self.area_type)
            if area_info is None:
                raise ValueError(f"Invalid area type: {self.area_type}")

            # Filter data based on the chosen model and area_id
            db_model = area_info['model']
            if db_model:
                if self.area_type == 'country':
                    db_data = db_model.objects.filter(
                        year__range=(int(start_year), int(end_year))
                    )
                else:
                    field_name = area_info['field_name']
                    db_data = db_model.objects.filter(
                        **{field_name: self.area_id},
                        year__range=(int(start_year), int(end_year))
                    )

                # Serialize data using the appropriate serializer
                serializer_class = area_info['serializer']
                serializer = serializer_class(db_data, many=True)
                data = serializer.data
                # Transform the data into the desired format
                transformed_data = {str(entry['year']): float(entry['areaHa']) for entry in data}
                # print(transformed_data)
            else:
                transformed_data = {'error': f"No model defined for area type: {self.area_type}"}

        except Exception as e:
            transformed_data = {'error': str(e)}

        return transformed_data

    def get_fire_hotspot_stat(self, start_year, end_year):
        try:
            # Use a dictionary to map area types to model classes and serializers
            area_type_mapping = {
                'country': {'model': FireHotspotNational, 'serializer': FireHotspotNationalSerializer, 'field_name': 'country'},
                'province': {'model': FireHotspotProvince, 'serializer': FireHotspotProvinceSerializer, 'field_name': 'gid'},
                'district': {'model': FireHotspotDistrict, 'serializer': FireHotspotDistrictSerializer, 'field_name': 'dist_code'},
                'protected_area': {'model': FireHotspotProtectedArea, 'serializer': FireHotspotProtectedAreaSerializer, 'field_name': 'pid'},
            }

            # Retrieve the corresponding model class and serializer based on area type
            area_info = area_type_mapping.get(self.area_type)
            if area_info is None:
                raise ValueError(f"Invalid area type: {self.area_type}")

            # Filter data based on the chosen model and area_id
            db_model = area_info['model']
            if db_model:
                if self.area_type == 'country':
                    db_data = db_model.objects.filter(
                        year__range=(int(start_year), int(end_year))
                    )
                else:
                    field_name = area_info['field_name']
                    db_data = db_model.objects.filter(
                        **{field_name: self.area_id},
                        year__range=(int(start_year), int(end_year))
                    )

                # Serialize data using the appropriate serializer
                serializer_class = area_info['serializer']
                serializer = serializer_class(db_data, many=True)
                data = serializer.data
                # Transform the data into the desired format
                transformed_data = {str(entry['year']): float(entry['fireNum']) for entry in data}
                # print(transformed_data)
            else:
                transformed_data = {'error': f"No model defined for area type: {self.area_type}"}

        except Exception as e:
            transformed_data = {'error': str(e)}

        return transformed_data




