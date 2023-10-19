import os, ee, time, json
from datetime import datetime, timedelta, date
from ee.ee_exception import EEException
from django.http import JsonResponse
from django.conf import settings

class GEEApi():
    MMR_COUNTRY_BOUNDARY = settings.MMR_COUNTRY_BOUNDARY
    MMR_LANDCOVER = settings.MMR_LANDCOVER

    def __init__(self, area_type, area_id): 

        self.scale = 100

        if area_type == "draw":
            coords = []
            for items in eval(geom):
                coords.append([items[1],items[0]])
            self.geometry =  ee.FeatureCollection(ee.Geometry.Polygon(coords)).geometry()

        elif area_type == "upload":
            polygons = []
            for items in geom:
                polygons.append(ee.Geometry.Polygon(items))
            self.geometry =  ee.FeatureCollection(ee.Geometry.MultiPolygon(polygons)).geometry()

        elif area_type == "country":
            self.geometry = ee.FeatureCollection(GEEApi.MMR_COUNTRY_BOUNDARY ).geometry()

        # elif area_type == "protected_area":
        #     self.geometry = ee.FeatureCollection(GEEApi.PROTECTED_AREA).filter(ee.Filter.eq("map_id", area_id)).geometry()

        # elif area_type == "province":
        #     area_id = int(area_id)
        #     self.geometry = ee.FeatureCollection(GEEApi.CAMBODIA_PROVINCE_BOUNDARY).filter(ee.Filter.eq("gid", area_id)).geometry()

        # elif area_type == "district":
        #     self.geometry = ee.FeatureCollection(GEEApi.CAMBODIA_DISTRICT_BOUNDARY).filter(ee.Filter.eq("DIST_CODE", area_id)).geometry()

        #polygon area in square kilometers.
        self.geometryArea = self.geometry.area().divide(1000 * 1000)
        #polygon area in Hectare
        self.geometryArea = float(self.geometryArea.getInfo()) / 0.010000

    def getTileLayerUrl(self, ee_image_object):
        map_id = ee.Image(ee_image_object).getMapId()
        tile_url_template = str(map_id['tile_fetcher'].url_format)
        return tile_url_template

    # ====================== EVI ====================>
    # ------------------------------------------------------------------------->
    def calcPie(self,ref_start,ref_end,series_start,series_end):

        res = []

        # The scale at which to reduce the polygons for the brightness time series.
        REDUCTION_SCALE_METERS = 10000

        ref_start = str(ref_start) + '-01-01'
        ref_end = str(ref_end) + '-12-31'
        series_start = str(series_start) + '-01-01'
        series_end = str(series_end) + '-12-31'

        cumulative = self.Calculation(ref_start,ref_end,series_start,series_end)

        myList = cumulative.toList(500)

        fit = ee.Image(myList.get(-1))

        months = ee.Date(series_end).difference(ee.Date(series_start),"month").getInfo()

        Threshold1 = months * 0.04
        Threshold2 = months * 0.02

        Threshold3 = months * -0.02
        Threshold4 = months * -0.04

        #area in hectare unit
        T1 = fit.where(fit.lt(Threshold1),0)
        T1 = T1.where(T1.gt(0),1).reduceRegion(ee.Reducer.sum(), self.geometry, REDUCTION_SCALE_METERS).getInfo()['EVI'] * (REDUCTION_SCALE_METERS * REDUCTION_SCALE_METERS) * 0.0001

        T2 = fit.where(fit.lt(Threshold2),0)
        T2 = T2.where(T2.gt(0),1).reduceRegion(ee.Reducer.sum(), self.geometry, REDUCTION_SCALE_METERS).getInfo()['EVI'] * (REDUCTION_SCALE_METERS * REDUCTION_SCALE_METERS) * 0.0001

        T3 = fit.where(fit.gt(Threshold3),0)
        T3 = T3.where(T3.lt(0),1).reduceRegion(ee.Reducer.sum(), self.geometry, REDUCTION_SCALE_METERS).getInfo()['EVI'] * (REDUCTION_SCALE_METERS * REDUCTION_SCALE_METERS) * 0.0001

        T4 = fit.where(fit.gt(Threshold4),0)
        T4 = T4.where(T4.lt(0),1).reduceRegion(ee.Reducer.sum(), self.geometry, REDUCTION_SCALE_METERS).getInfo()['EVI'] * (REDUCTION_SCALE_METERS * REDUCTION_SCALE_METERS) * 0.0001

        T5 = fit.where(fit.gt(-9999),1).reduceRegion(ee.Reducer.sum(), self.geometry, REDUCTION_SCALE_METERS).getInfo()['EVI'] * (REDUCTION_SCALE_METERS * REDUCTION_SCALE_METERS) * 0.0001


        p1 = float('%.2f' % (T1))
        p2 = float('%.2f' % ((T2 - T1)))

        m1 = float('%.2f' % (T4))
        m2 = float('%.2f' % ((T3 - T4)))

        middle = float('%.2f' % ((T5 - p1 - p2 - m1 - m2)))

        myArray = [p1,p2,middle,m2,m1]
        return myArray
        
    def Calculation(self, ref_start,ref_end,series_start,series_end):
        IMAGE_COLLECTION_ID = ee.ImageCollection('MODIS/006/MYD13A1')
        collection = ee.ImageCollection(IMAGE_COLLECTION_ID) #.filterDate('2008-01-01', '2010-12-31').sort('system:time_start')
        reference = collection.filterDate(ref_start,ref_end ).sort('system:time_start').select('EVI')
        series = collection.filterDate(series_start, series_end).sort('system:time_start').select('EVI')

        def calcMonthlyMean(img):

          # get the month of the map
          month = ee.Number.parse(ee.Date(img.get("system:time_start")).format("M"))
          # get the day in month
          day = ee.Number.parse(ee.Date(img.get("system:time_start")).format("d"))

          # select image in reference period
          refmaps = reference.filter(ee.Filter.calendarRange(month,month,"Month"))
          refmaps = refmaps.filter(ee.Filter.calendarRange(day,day,"day_of_month"))
          # get the mean of the reference
          refmean = ee.Image(refmaps.mean()).multiply(0.0001)

          # get date
          time = img.get('system:time_start')

          # multiply image by scaling factor
          study = img.multiply(0.0001)

          # subtract mean from study
          result = ee.Image(study.subtract(refmean).set('system:time_start',time))

          return result

        mycollection = series.map(calcMonthlyMean)

        time0 = series.first().get('system:time_start')
        first = ee.List([ee.Image(0).set('system:time_start', time0).select([0], ['EVI'])])

        ## This is a function to pass to Iterate().
        ## As anomaly images are computed, add them to the list.
        def accumulate(image, mylist):
            ## Get the latest cumulative anomaly image from the end of the list with
            ## get(-1).  Since the type of the list argument to the function is unknown,
            ## it needs to be cast to a List.  Since the return type of get() is unknown,
            ## cast it to Image.
            previous = ee.Image(ee.List(mylist).get(-1))
            ## Add the current anomaly to make a new cumulative anomaly image.
            added = image.unmask(0).add(previous).set('system:time_start', image.get('system:time_start'))
            ## Propagate metadata to the new image.
            #
            ## Return the list with the cumulative anomaly inserted.
            return ee.List(mylist).add(added)

        ## Create an ImageCollection of cumulative anomaly images by iterating.
        ## Since the return type of iterate is unknown, it needs to be cast to a List.
        cumulative = ee.ImageCollection(ee.List(mycollection.iterate(accumulate, first)))

        return cumulative

    # --------------------------------------------------------------------------->
    def GetPolygonTimeSeries(self,ref_start,ref_end,series_start,series_end):
        """Returns details about the polygon with the passed-in ID."""


        #details = memcache.get(polygon_id)

        # If we've cached details for this polygon, return them.
        #if details is not None:
        #  return details

        details = {}

        try:
            details['timeSeries'] = self.ComputePolygonTimeSeries(ref_start,ref_end,series_start,series_end)
        # Store the results in memcache.
        #memcache.add(polygon_id, json.dumps(details), MEMCACHE_EXPIRATION)
        except ee.EEException as e:
        # Handle exceptions from the EE client library.
            details['error'] = str(e)

        # Send the results to the browser.
        # print(details)
        return details

    def ComputePolygonTimeSeries(self,ref_start,ref_end,series_start,series_end):

        """Returns a series of brightness over time for the polygon."""
        ref_start = str(ref_start) + '-01-01'
        ref_end = str(ref_end) + '-12-31'
        series_start = str(series_start) + '-01-01'
        series_end = str(series_end) + '-12-31'

        cumulative = self.Calculation(ref_start,ref_end,series_start,series_end)

        REDUCTION_SCALE_METERS = 10000

        # Compute the mean brightness in the region in each image.
        def ComputeMean(img):
            reduction = img.reduceRegion(
                ee.Reducer.mean(), self.geometry, REDUCTION_SCALE_METERS)
            return ee.Feature(None, {
                'EVI': reduction.get('EVI'),
                'system:time_start': img.get('system:time_start')
            })

        # Extract the results as a list of lists.
        def ExtractMean(feature):
            return [
                feature['properties']['system:time_start'],
                feature['properties']['EVI']
            ]


        chart_data = cumulative.map(ComputeMean).getInfo()
        res = []
        for feature in chart_data['features']:
            res.append(ExtractMean(feature))
        # print(res)
        return res

    # --------------------------------------------------------------------------->
    def getEVIMap(self,ref_start,ref_end,series_start,series_end):
        ref_start = str(ref_start) + '-01-01'
        ref_end = str(ref_end) + '-12-31'
        series_start = str(series_start) + '-01-01'
        series_end = str(series_end) + '-12-31'

        cumulative = self.Calculation(ref_start,ref_end,series_start,series_end)

        myList = cumulative.toList(500)

        fit = ee.Image(myList.get(-1)).clip(self.geometry).select('EVI')
        image = fit.reproject(crs=fit.projection());        
        image = image.reproject(crs='EPSG:4326', scale=250) #250
        months = ee.Date(series_end).difference(ee.Date(series_start),"month").getInfo()

        Threshold1 = months * 0.1
        Threshold2 = months * -0.1
        eviMap = self.getTileLayerUrl(image.visualize(min= Threshold2, max=Threshold1, palette=['E76F51','F4A261','E9C46A','2A9D8F','264653']))
        
        return eviMap

    # -------------------------------------------------------------------------
    def getDownloadEVIMap(self,ref_start,ref_end,series_start,series_end):
        ref_start = str(ref_start) + '-01-01'
        ref_end = str(ref_end) + '-12-31'
        series_start = str(series_start) + '-01-01'
        series_end = str(series_end) + '-12-31'
        cumulative = self.Calculation(ref_start,ref_end,series_start,series_end)
        myList = cumulative.toList(500)
        fit = ee.Image(myList.get(-1)).clip(self.geometry)
        
        try:
            dnldURL = fit.getDownloadURL({
                    'name': 'evi'+series_start+'-'+series_end,
                    'scale': 1000,
                    'crs': 'EPSG:4326',
                    'region': self.geometry
                })

            return {
                'downloadURL': dnldURL,
                'success': 'success'
            }
        except Exception as e:
            return {
                'success': 'not success'
            }

    #===================== LandCover ==========================*/
    LANDCOVERCLASSES = [
        {
            'name': 'Unknown',
            'value': '0',
            'color': '6f6f6f'
        },
        {
            'name': 'Surface Water',
            'value': '1',
            'color': '0000ff'
        },
        {
            'name': 'Snow and Ice',
            'value': '2',
            'color': '808080'
        },
        {
            'name': 'Mangroves',
            'value': '3',
            'color': '556b2f'
        },
        {
            'name': 'Cropland',
            'value': '4',
            'color': '7cfc00'
        },
        {
            'name': 'Urban and Built up',
            'value': '5',
            'color': '8b0000'
        },
        {
            'name': 'Grassland',
            'value': '6',
            'color': '20b2aa'
        },
        {
            'name': 'Closed Forest',
            'value': '7',
            'color': '006400'
        },
        {
            'name': 'Open Forest',
            'value': '8',
            'color': '90ee90'
        },
        {
            'name': 'Wetland',
            'value': '9',
            'color': '42f4c2'
        },
        {
            'name': 'Woody',
            'value': '10',
            'color': '8b4513'
        },
        {
            'name': 'Other land',
            'value': '11',
            'color': '6f6f6f'
        }
    ]

    INDEX_CLASS = {}
    for _class in LANDCOVERCLASSES:
        INDEX_CLASS[int(_class['value'])] = _class['name']

    def getLandCoverMap(self, year):
        landCoverIC = ee.ImageCollection(GEEApi.MMR_LANDCOVER)
        image = landCoverIC.filterDate('%s-01-01' % year,'%s-12-31' % year).mean()
        image = image.select('classification')

        # Start with creating false boolean image
        masked_image = image.eq(ee.Number(100))

        classes=range(0, 11)

        # get the classes
        for _class in classes:
            _mask = image.eq(ee.Number(int(_class)))
            masked_image = masked_image.add(_mask)
        palette = []
        for _class in GEEApi.LANDCOVERCLASSES:
            palette.append(_class['color'])

        palette = ','.join(palette)

        image = image.updateMask(masked_image).clip(self.geometry)
        lcMap = self.getTileLayerUrl(image.visualize(min=0, max=str(len(GEEApi.LANDCOVERCLASSES) - 1), palette=palette))
        return lcMap