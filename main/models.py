from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import string
import random
import hashlib

class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key_name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Check if key is already set, and if so, do not generate a new key
        if not self.key:
            # Generate a new complex API key based on key_name if it's provided
            if self.key_name:
                self.key = self.generate_complex_api_key(f"{str(self.user.username)}.")

        super(APIKey, self).save(*args, **kwargs)

    def generate_complex_api_key(self, prefix, length=64):
        # Define character set for random characters
        characters = string.ascii_letters + string.digits

        # Calculate the number of random characters needed
        num_random_chars = length - len(prefix)

        if num_random_chars <= 0:
            raise ValueError("API key length must be greater than the length of the prefix")

        # Generate random characters
        random_chars = ''.join(random.choice(characters) for _ in range(num_random_chars))

        # Combine prefix and random characters to create the API key
        api_key = prefix + random_chars

        return api_key

    def set_raw_api_key(self, raw_api_key):
        # Set the raw API key value (used on the frontend)
        self.raw_api_key = raw_api_key

    def save_hashed_api_key(self):
        # Hash the raw API key and store it as the hashed API key
        if hasattr(self, 'raw_api_key') and self.raw_api_key:
            self.key = self.hash_api_key(self.raw_api_key)
        else:
            raise ValueError("Raw API key is missing")

    def hash_api_key(self, input_str):
        # Hash the input string using a strong cryptographic hash function (e.g., SHA-256)
        return hashlib.sha256(input_str.encode()).hexdigest()

class LandCoverNational(models.Model):
    country = models.CharField(max_length=100)
    landcover = models.CharField(max_length=100)
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Land Cover National'

    def __str__(self):
        return self.country

class LandCoverProvince(models.Model):
    province = models.CharField(max_length=100, null=True, blank=True)
    gid = models.IntegerField()
    landcover = models.CharField(max_length=100)
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Land Cover Province'

    def __str__(self):
        return self.province

class LandCoverDistrict(models.Model):
    district = models.CharField(max_length=100)
    dist_code = models.CharField(max_length=50)
    landcover = models.CharField(max_length=100)
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Land Cover District'

    def __str__(self):
        return self.district

class LandCoverProtectedArea(models.Model):
    protected_area = models.CharField(max_length=100)
    pid = models.CharField(max_length=50)
    landcover = models.CharField(max_length=100)
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Land Cover Protected Area'

    def __str__(self):
        return self.protected_area

class GLADAlertNational(models.Model):
    country = models.CharField(max_length=100)
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'GLAD Alert National'

    def __str__(self):
        return self.country

class GLADAlertProvince(models.Model):
    province = models.CharField(max_length=100, null=True, blank=True)
    gid = models.IntegerField()
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'GLAD Alert Province'

    def __str__(self):
        return self.province

class GLADAlertDistrict(models.Model):
    district = models.CharField(max_length=100)
    dist_code = models.CharField(max_length=50)
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name_plural = 'GLAD Alert District'

    def __str__(self):
        return self.district

class GLADAlertProtectedArea(models.Model):
    protected_area = models.CharField(max_length=100)
    pid = models.CharField(max_length=50)
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'GLAD Alert Protected Area'

    def __str__(self):
        return self.protected_area

class SARAlertNational(models.Model):
    country = models.CharField(max_length=100)
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'SAR Alert National'

    def __str__(self):
        return self.country

class SARAlertProvince(models.Model):
    province = models.CharField(max_length=100, null=True, blank=True)
    gid = models.IntegerField()
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'SAR Alert Province'

    def __str__(self):
        return self.province

class SARAlertDistrict(models.Model):
    district = models.CharField(max_length=100)
    dist_code = models.CharField(max_length=50)
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name_plural = 'SAR Alert District'

    def __str__(self):
        return self.district

class SARAlertProtectedArea(models.Model):
    protected_area = models.CharField(max_length=100)
    pid = models.CharField(max_length=50)
    year = models.IntegerField()
    areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'SAR Alert Protected Area'

    def __str__(self):
        return self.protected_area

class FireHotspotNational(models.Model):
    country = models.CharField(max_length=100)
    year = models.IntegerField()
    fireNum = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Fire Hotspot National'

    def __str__(self):
        return self.country

class FireHotspotProvince(models.Model):
    province = models.CharField(max_length=100, null=True, blank=True)
    gid = models.IntegerField()
    year = models.IntegerField()
    fireNum = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Fire Hotspot Province'

    def __str__(self):
        return self.province

class FireHotspotDistrict(models.Model):
    district = models.CharField(max_length=100)
    dist_code = models.CharField(max_length=50)
    year = models.IntegerField()
    fireNum = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name_plural = 'Fire Hotspot District'

    def __str__(self):
        return self.district

class FireHotspotProtectedArea(models.Model):
    protected_area = models.CharField(max_length=100)
    pid = models.CharField(max_length=50)
    year = models.IntegerField()
    fireNum = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Fire Hotspot Protected Area'

    def __str__(self):
        return self.protected_area

class ForestCoverNational(models.Model):
    country = models.CharField(max_length=100)
    year = models.IntegerField()
    forest_areaHa = models.DecimalField(max_digits=10, decimal_places=2)
    nonforest_areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Forest Cover National'

    def __str__(self):
        return self.country

class ForestCoverProvince(models.Model):
    province = models.CharField(max_length=100, null=True, blank=True)
    gid = models.IntegerField()
    year = models.IntegerField()
    forest_areaHa = models.DecimalField(max_digits=10, decimal_places=2)
    nonforest_areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Forest Cover Province'

    def __str__(self):
        return self.province

class ForestCoverDistrict(models.Model):
    district = models.CharField(max_length=100)
    dist_code = models.CharField(max_length=50)
    year = models.IntegerField()
    forest_areaHa = models.DecimalField(max_digits=10, decimal_places=2)
    nonforest_areaHa = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name_plural = 'Forest Cover District'

    def __str__(self):
        return self.district

class ForestCoverProtectedArea(models.Model):
    protected_area = models.CharField(max_length=100)
    pid = models.CharField(max_length=50)
    year = models.IntegerField()
    forest_areaHa = models.DecimalField(max_digits=10, decimal_places=2)
    nonforest_areaHa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Forest Cover Protected Area'

    def __str__(self):
        return self.protected_area

class ForestChagesCountry(models.Model):
    country = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField()
    built = models.DecimalField(max_digits=10, decimal_places=2)
    mangrove = models.DecimalField(max_digits=10, decimal_places=2)
    otherPlantation = models.DecimalField(max_digits=10, decimal_places=2)
    water = models.DecimalField(max_digits=10, decimal_places=2)
    shrub = models.DecimalField(max_digits=10, decimal_places=2)
    rice = models.DecimalField(max_digits=10, decimal_places=2)
    cropland = models.DecimalField(max_digits=10, decimal_places=2)
    grass = models.DecimalField(max_digits=10, decimal_places=2)
    evergreen = models.DecimalField(max_digits=10, decimal_places=2)
    deciduous = models.DecimalField(max_digits=10, decimal_places=2)
    wetland = models.DecimalField(max_digits=10, decimal_places=2)
    rubber = models.DecimalField(max_digits=10, decimal_places=2)
    floodedForest = models.DecimalField(max_digits=10, decimal_places=2)
    semievergreen = models.DecimalField(max_digits=10, decimal_places=2)
    village = models.DecimalField(max_digits=10, decimal_places=2)
    others = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Forest Changes country lavel'

    def __str__(self):
        return self.country

class ForestChagesProvince(models.Model):
    province = models.CharField(max_length=100, null=True, blank=True)
    gid = models.IntegerField()
    year = models.IntegerField()
    built = models.DecimalField(max_digits=10, decimal_places=2)
    mangrove = models.DecimalField(max_digits=10, decimal_places=2)
    otherPlantation = models.DecimalField(max_digits=10, decimal_places=2)
    water = models.DecimalField(max_digits=10, decimal_places=2)
    shrub = models.DecimalField(max_digits=10, decimal_places=2)
    rice = models.DecimalField(max_digits=10, decimal_places=2)
    cropland = models.DecimalField(max_digits=10, decimal_places=2)
    grass = models.DecimalField(max_digits=10, decimal_places=2)
    evergreen = models.DecimalField(max_digits=10, decimal_places=2)
    deciduous = models.DecimalField(max_digits=10, decimal_places=2)
    wetland = models.DecimalField(max_digits=10, decimal_places=2)
    rubber = models.DecimalField(max_digits=10, decimal_places=2)
    floodedForest = models.DecimalField(max_digits=10, decimal_places=2)
    semievergreen = models.DecimalField(max_digits=10, decimal_places=2)
    village = models.DecimalField(max_digits=10, decimal_places=2)
    others = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Forest changes province level'

    def __str__(self):
        return self.province
    
class ForestChagesDistrict(models.Model):
    district = models.CharField(max_length=100, null=True, blank=True)
    dist_code = models.IntegerField()
    year = models.IntegerField()
    built = models.DecimalField(max_digits=10, decimal_places=2)
    mangrove = models.DecimalField(max_digits=10, decimal_places=2)
    otherPlantation = models.DecimalField(max_digits=10, decimal_places=2)
    water = models.DecimalField(max_digits=10, decimal_places=2)
    shrub = models.DecimalField(max_digits=10, decimal_places=2)
    rice = models.DecimalField(max_digits=10, decimal_places=2)
    cropland = models.DecimalField(max_digits=10, decimal_places=2)
    grass = models.DecimalField(max_digits=10, decimal_places=2)
    evergreen = models.DecimalField(max_digits=10, decimal_places=2)
    deciduous = models.DecimalField(max_digits=10, decimal_places=2)
    wetland = models.DecimalField(max_digits=10, decimal_places=2)
    rubber = models.DecimalField(max_digits=10, decimal_places=2)
    floodedForest = models.DecimalField(max_digits=10, decimal_places=2)
    semievergreen = models.DecimalField(max_digits=10, decimal_places=2)
    village = models.DecimalField(max_digits=10, decimal_places=2)
    others = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Forest changes district level'

    def __str__(self):
        return self.district
    

class ForestChagesProtectedArea(models.Model):
    protected_area = models.CharField(max_length=100, null=True, blank=True)
    pid = models.CharField(max_length=50)
    year = models.IntegerField()
    built = models.DecimalField(max_digits=10, decimal_places=2)
    mangrove = models.DecimalField(max_digits=10, decimal_places=2)
    otherPlantation = models.DecimalField(max_digits=10, decimal_places=2)
    water = models.DecimalField(max_digits=10, decimal_places=2)
    shrub = models.DecimalField(max_digits=10, decimal_places=2)
    rice = models.DecimalField(max_digits=10, decimal_places=2)
    cropland = models.DecimalField(max_digits=10, decimal_places=2)
    grass = models.DecimalField(max_digits=10, decimal_places=2)
    evergreen = models.DecimalField(max_digits=10, decimal_places=2)
    deciduous = models.DecimalField(max_digits=10, decimal_places=2)
    wetland = models.DecimalField(max_digits=10, decimal_places=2)
    rubber = models.DecimalField(max_digits=10, decimal_places=2)
    floodedForest = models.DecimalField(max_digits=10, decimal_places=2)
    semievergreen = models.DecimalField(max_digits=10, decimal_places=2)
    village = models.DecimalField(max_digits=10, decimal_places=2)
    others = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Forest changes on protected area'

    def __str__(self):
        return self.protected_area