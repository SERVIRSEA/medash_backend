from rest_framework import serializers
from .models import *

class LandCoverNationalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandCoverNational
        fields = ['landcover', 'year', 'areaHa']

class LandCoverProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandCoverProvince
        fields = ['landcover', 'year', 'areaHa']

class LandCoverDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandCoverDistrict
        fields = ['landcover', 'year', 'areaHa']

class LandCoverProtectedAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandCoverProtectedArea
        fields = ['landcover', 'year', 'areaHa']

class ForestCoverNationalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForestCoverNational
        fields = ['year', 'forest_areaHa', 'nonforest_areaHa']

class ForestCoverProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForestCoverProvince
        fields = ['year', 'forest_areaHa', 'nonforest_areaHa']

class ForestCoverDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForestCoverDistrict
        fields = ['year', 'forest_areaHa', 'nonforest_areaHa']

class ForestCoverProtectedAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForestCoverProtectedArea
        fields = ['year', 'forest_areaHa', 'nonforest_areaHa']

class SARAlertNationalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SARAlertNational
        fields = ['year', 'areaHa']

class SARAlertProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SARAlertProvince
        fields = ['year', 'areaHa']

class SARAlertDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = SARAlertDistrict
        fields = ['year', 'areaHa']

class SARAlertProtectedAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SARAlertProtectedArea
        fields = ['year', 'areaHa']

class GLADAlertNationalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GLADAlertNational
        fields = ['year', 'areaHa']

class GLADAlertProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GLADAlertProvince
        fields = ['year', 'areaHa']

class GLADAlertDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = GLADAlertDistrict
        fields = ['year', 'areaHa']

class GLADAlertProtectedAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GLADAlertProtectedArea
        fields = ['year', 'areaHa']

class FireHotspotNationalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FireHotspotNational
        fields = ['year', 'fireNum']

class FireHotspotProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FireHotspotProvince
        fields = ['year', 'fireNum']

class FireHotspotDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = FireHotspotDistrict
        fields = ['year', 'fireNum']

class FireHotspotProtectedAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FireHotspotProtectedArea
        fields = ['year', 'fireNum']