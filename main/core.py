import os, ee, time, json
from datetime import datetime, timedelta, date
from ee.ee_exception import EEException
from django.http import JsonResponse
from django.conf import settings

class GEEApi():
    TREE_CANOPY = ee.ImageCollection(settings.TREE_CANOPY)
    TREE_HEIGHT = ee.ImageCollection(settings.TREE_HEIGHT)
    GLAD_ALERT = settings.GLAD_ALERT
    GLAD_FOREST_ALERT_FC = settings.GLAD_FOREST_ALERT_FC
    CAMBODIA_COUNTRY_BOUNDARY = settings.CAMBODIA_COUNTRY_BOUNDARY
    PROTECTED_AREA = settings.PROTECTED_AREA
    CAMBODIA_PROVINCE_BOUNDARY = settings.CAMBODIA_PROVINCE_BOUNDARY
    CAMBODIA_DISTRICT_BOUNDARY = settings.CAMBODIA_DISTRICT_BOUNDARY
    BURNED_AREA = ee.ImageCollection(settings.BURNED_AREA)
    FIRMS_BURNED_AREA = ee.ImageCollection(settings.FIRMS_BURNED_AREA)
    LANDCOVER = ee.ImageCollection(settings.LANDCOVER)
    SAR_ALERT = settings.SAR_ALERT

    COLOR = ['A8D9C6','B0DAB2','BFE1C9','AAD7A0','C3DE98','D5E59E','93D2BF','95CF9C','A4D7B8','9BD291','B1D78A','C9E08E','5CC199','77C78C','37B54A','126039','146232','0F8040','279445','449644','59A044','0E361E','236832','335024', '36461F']
    COLORFORESTALERT = ['943126', 'B03A2E', 'CB4335', 'E74C3C', 'F1948A', 'F5B7B1','943126', 'B03A2E', 'CB4335', 'E74C3C', 'F1948A', 'F5B7B1']
    COLORSARALERT = ['fba004', 'f9bc16', 'ac9d0a', 'fba004', 'f9bc16', 'ac9d0a','fba004', 'f9bc16', 'ac9d0a','fba004', 'f9bc16', 'ac9d0a']

    geometry = ee.FeatureCollection(CAMBODIA_COUNTRY_BOUNDARY).geometry()

    def __init__(self, area_type, area_id): # area_path, area_name, geom, 

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
            self.geometry = ee.FeatureCollection(GEEApi.CAMBODIA_COUNTRY_BOUNDARY).filter(ee.Filter.eq("NAME_ENGLI", area_id)).geometry()

        elif area_type == "protected_area":
            self.geometry = ee.FeatureCollection(GEEApi.PROTECTED_AREA).filter(ee.Filter.eq("map_id", area_id)).geometry()

        elif area_type == "province":
            area_id = int(area_id)
            self.geometry = ee.FeatureCollection(GEEApi.CAMBODIA_PROVINCE_BOUNDARY).filter(ee.Filter.eq("gid", area_id)).geometry()

        elif area_type == "district":
            self.geometry = ee.FeatureCollection(GEEApi.CAMBODIA_DISTRICT_BOUNDARY).filter(ee.Filter.eq("DIST_CODE", area_id)).geometry()

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
        image = image.reproject(crs='EPSG:4326', scale=250)
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

    # ====================== Landcover ====================>
    # -------------------------------------------------------------------------
    def getLandCoverMap(self, year):
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv3/"+str(year)).clip(self.geometry)
        classNames = ['evergreen', 'semi-evergreen', 'deciduous', 'mangrove', 'flooded forest','rubber', 'other plantations', 'rice', 'cropland', 'surface water', 'grassland', 'woodshrub', 'built-up area', 'village', 'other']
        palette = ['267300', '38A800', '70A800', '00A884', 'B4D79E', 'AAFF00', 'F5F57A', 'FFFFBE', 'FFD37F', '004DA8', 'D7C29E', '89CD66', 'E600A9', 'A900E6', '6f6f6f']
        lcMap = self.getTileLayerUrl(lcImage.visualize(min=0, max=str(len(classNames)-1), palette=palette))
        return lcMap
    
    # -------------------------------------------------------------------------
    def getDownloadLandcoverMap(self, year):
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv3/"+str(year)).clip(self.geometry)
        try:
            dnldURL = lcImage.getDownloadURL({
                'name': 'LC'+year,
                'scale': 100,
                'crs': 'EPSG:4326'
            })
            return {
                'downloadURL': dnldURL,
                'success': 'success'
            }
            # print(dnldURL)
        except Exception as e:
            return {
                'success': 'not success'
            }
            # print(e)

    # -------------------------------------------------------------------------
    def calLandcoverArea(self, series_start, series_end, year):
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv3/"+str(year)).clip(self.geometry)
        IC= GEEApi.LANDCOVER.filterBounds(self.geometry).sort('system:time_start', False).filterDate(series_start, series_end)
        LANDCOVERCLASSES = [
            {'name':'evergreen' ,'number': 0, 'color': '267300'},
            {'name':'semi-evergreen' ,'number': 1, 'color': '38A800'},
            {'name':'deciduous' ,'number': 2, 'color': '70A800'},
            {'name':'mangrove' ,'number': 3, 'color': '00A884'},
            {'name':'flooded forest' ,'number': 4, 'color': 'B4D79E'},
            {'name':'rubber' ,'number': 5, 'color': 'AAFF00'},
            {'name':'other plantations' ,'number': 6, 'color': 'F5F57A'},
            {'name':'rice' ,'number': 7, 'color': 'FFFFBE'},
            {'name':'cropland' ,'number': 8, 'color': 'FFD37F'},
            {'name':'surface water' ,'number': 9, 'color': '004DA8'},
            {'name':'grassland' ,'number': 10, 'color': 'D7C29E'},
            {'name':'woodshrub' ,'number': 11, 'color': '89CD66'},
            {'name':'built-up area' ,'number': 12, 'color': 'E600A9'},
            {'name':'village' ,'number': 13, 'color': 'A900E6'},
            {'name':'other' ,'number': 14, 'color': '6f6f6f'}
        ]

        INDEX_CLASS = {}
        for _class in LANDCOVERCLASSES:
            INDEX_CLASS[int(_class['number'])] = _class['name']

        AreaClass= {}
        class_areas = ee.Image.pixelArea().addBands(lcImage).reduceRegion(
            reducer= ee.Reducer.sum().group(
                groupField= 1,
                groupName= 'code',
            ),
            geometry= self.geometry,
            scale= 100,  # sample the geometry at 1m intervals
            maxPixels= 1e15
        )

        data = class_areas.getInfo()['groups']
        for item in data:
            #area hetare
            AreaClass[INDEX_CLASS[int(item['code'])]] = float('{0:.2f}'.format(item['sum']/10000))

        lcarea = AreaClass
        return lcarea

    # -------------------------------------------------------------------------
    def getLandcoverArea(self, start_year, end_year):
        res = {}
        # print(type(start_year))
        for year in range(int(start_year), int(end_year)+1):
            series_start = str(year) + '-01-01'
            series_end = str(year) + '-12-31'
            res[str(year)] = self.calLandcoverArea(series_start, series_end, year)
        return res

    # ====================== Landcover Rice ====================>
    # -------------------------------------------------------------------------
    def getLandCoverRiceMap(self, year):
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv3/"+str(year)).eq(7).clip(self.geometry).selfMask()
        palette = ['FFFFFF','FFFF00']
        lcRiceMap = self.getTileLayerUrl(lcImage.visualize(min=0, max=1, palette=palette))
        return lcRiceMap

    def downloadLandcoverRiceMap(self, year):
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv3/"+str(year)).eq(7).clip(self.geometry)
        try:
            dnldURL = lcImage.getDownloadURL({
                'name': 'LCRICE'+year,
                'scale': 100,
                'crs': 'EPSG:4326'
            })
            return {
                'downloadURL': dnldURL,
                'success': 'success'
            }
            # print(dnldURL)
        except Exception as e:
            return {
                'success': 'not success'
            }
            # print(e)

    def calRiceTimeSeries(self, series_start, series_end, year):
        total_area = self.calLandcoverArea(series_start, series_end, year)
        rice_area = total_area["rice"]
        return rice_area

    def getLandcoverRiceArea(self, start_year, end_year): 
        res = {}
        # print(end_year)
        start_year = int(start_year)
        end_year = int(end_year)

        if end_year >=2021:
            end_year = 2020
        else:
            end_year = end_year

        for year in range(start_year, end_year+1):
            series_start = str(year) + '-01-01'
            series_end = str(year) + '-12-31'
            res[str(year)] = self.calRiceTimeSeries(series_start, series_end, year)
        # print(res)
        return res


    # ====================== Landcover Rubber ====================>
    # -------------------------------------------------------------------------
    def getLandCoverRubberMap(self, year):
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv3/"+str(year)).eq(5).clip(self.geometry).selfMask()
        palette = ['FFFFFF','AAFF00']
        lcRubberMap = self.getTileLayerUrl(lcImage.visualize(min=0, max=1, palette=palette))
        return lcRubberMap

    def downloadLandcoverRubberMap(self, year):
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv3/"+str(year)).eq(5).clip(self.geometry)
        try:
            dnldURL = lcImage.getDownloadURL({
                'name': 'LCRUBBER'+year,
                'scale': 100,
                'crs': 'EPSG:4326'
            })
            return {
                'downloadURL': dnldURL,
                'success': 'success'
            }
            # print(dnldURL)
        except Exception as e:
            return {
                'success': 'not success'
            }
            # print(e)

    def calRubberTimeSeries(self, series_start, series_end, year):
        total_area = self.calLandcoverArea(series_start, series_end, year)
        rubber_area = total_area["rubber"]
        return rubber_area

    def getLandcoverRubberArea(self, start_year, end_year): 
        res = {}
        start_year = int(start_year)
        end_year = int(end_year)

        if end_year >=2021:
            end_year = 2020
        else:
            end_year = end_year

        for year in range(start_year, end_year+1):
            series_start = str(year) + '-01-01'
            series_end = str(year) + '-12-31'
            res[str(year)] = self.calRubberTimeSeries(series_start, series_end, year)
        # print(res)
        return res

    #=============================== Forest Alert =======================>
    #---------------------------------------------------------------------
    def getForestAlertMap(self, year):
        if year == 2022:
            glad =  ee.ImageCollection('projects/glad/alert/UpdResult').select(['alertDate22']) 
            GLADIC = glad.filterBounds(self.geometry)#.filterDate(series_start, series_end)
            image = GLADIC.sort('system:time_start', False).first().clip(self.geometry).toInt16()
            binary_image = image.rename(['binary']).selfMask()
        else:
            GLADIC = ee.ImageCollection(GEEApi.GLAD_ALERT).filterBounds(self.geometry).filterDate(series_start, series_end)
            image = GLADIC.sort('system:time_start', False).first().select("alert").clip(self.geometry).toInt16()
            binary_image = image.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()
        
        colorMap = GEEApi.COLORFORESTALERT[colorIndex]
        alertMap = self.getTileLayerUrl(binary_image.visualize(min=0, max=1, palette=colorMap))
        return lcRiceMap
    
    #------------------------------------------------------------------------------------
    def getSARAlertMap(self, year):
        if year == 2021:
            image = ee.Image('projects/cemis-camp/assets/sarAlert/alert_2021V4')
            image = image.select("landclass").clip(self.geometry).toInt16()
            binary_image = image.rename(['binary']).selfMask()
        elif year == 2022:
            image = ee.Image('projects/cemis-camp/assets/sarAlert/alert_2022V4')
            image = image.select("landclass").clip(self.geometry).toInt16()
            binary_image = image.rename(['binary']).selfMask()
        else: 
            series_start = str(year) + '-01-01'
            series_end = str(year) + '-12-31'
            SARIC = ee.ImageCollection(GEEApi.SAR_ALERT).filterBounds(self.geometry).filterDate(series_start, series_end)
            # image = ee.Image(GEEApi.SAR_ALERT+"/"+"alert_"+str(year))
            image = SARIC.sort('system:time_start', False).first()
            image = image.select("landclass").clip(self.geometry).toInt16()
            binary_image = image.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()

        colorMap = GEEApi.COLORSARALERT[colorIndex]
        sarAlertMap = self.getTileLayerUrl(binary_image.visualize(min=0, max=1, palette=colorMap))
        return sarAlertMap

    # -------------------------------------------------------------------------
    def downloadForestAlert(self, year):
        series_start = str(year) + '-01-01'
        series_end = str(year) + '-12-31'
        GLADIC = ee.ImageCollection(GEEApi.GLAD_ALERT).filterBounds(self.geometry).filterDate(series_start, series_end)
        image = GLADIC.sort('system:time_start', False).first().select("alert").clip(self.geometry).toInt16()
        binary_image = image.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()

        try:
            dnldURL = binary_image.getDownloadURL({
                    'name': 'ForestAlert'+year,
                    'scale': 100,
                    'crs': 'EPSG:4326'
                })
            return {
                'downloadURL': dnldURL,
                'success': 'success'
                }
        except Exception as e:
            return {
                'success': 'not success'
            }

    # -------------------------------------------------------------------------
    def downloadSARAlert(self, year):
        series_start = str(year) + '-01-01'
        series_end = str(year) + '-12-31'
        
        SARIC = ee.ImageCollection(GEEApi.SAR_ALERT).filterBounds(self.geometry).filterDate(series_start, series_end)
        # image = ee.Image(GEEApi.SAR_ALERT+"/"+"alert_"+str(year))
        image = SARIC.sort('system:time_start', False).first()

        image = image.select("landclass").clip(self.geometry).toInt16()

        binary_image = image.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()

        try:
            dnldURL = binary_image.getDownloadURL({
                    'name': 'ForestAlert'+year,
                    'scale': 30,
                    'crs': 'EPSG:4326'
                })
            return {
                'downloadURL': dnldURL,
                'success': 'success'
                }
        except Exception as e:
            return {
                'success': 'not success'
            }

    #-------------------------------------------------------------------------
    def calForestAlert(self, series_start, series_end, year):
        if year == 2022:
            glad =  ee.ImageCollection('projects/glad/alert/UpdResult').select(['alertDate22']) 
            GLADIC = glad.filterBounds(self.geometry)
            image = GLADIC.sort('system:time_start', False).first().clip(self.geometry).toInt16()
            binary_image = image.rename(['binary']).selfMask()
        else:
            GLADIC = ee.ImageCollection(GEEApi.GLAD_ALERT).filterBounds(self.geometry).filterDate(series_start, series_end)
            image = GLADIC.sort('system:time_start', False).first().select("alert").clip(self.geometry).toInt16()
            binary_image = image.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()

        if area_type == "draw" or area_type == "upload":
            reducer = binary_image.multiply(900).reduceRegion(
                reducer= ee.Reducer.sum(),
                geometry= self.geometry,
                crs = 'EPSG:32647', # WGS Zone N 47
                scale= 30,
                maxPixels= 1E20
            )

            #area in squre meter
            stats = reducer.getInfo()['binary']
            #convert to hactare divide by 10000
            areaHA = stats / 10000
        else:
            if area_type == "country":
                forest_featurecol = ee.FeatureCollection(GEEApi.GLAD_FOREST_ALERT_FC+""+str(year)+"/cambodia_areaMeta")
                forest_alert = forest_featurecol.filter(ee.Filter.eq('NAME_ENGLI', area_id))
            elif area_type == "province":
                forest_featurecol = ee.FeatureCollection(GEEApi.GLAD_FOREST_ALERT_FC+""+str(year)+"/province_Metadata")
                forest_alert = forest_featurecol.filter(ee.Filter.eq('gid', area_id))
            elif area_type == "district":
                forest_featurecol = ee.FeatureCollection(GEEApi.GLAD_FOREST_ALERT_FC+""+str(year)+"/district_Metadata")
                forest_alert = forest_featurecol.filter(ee.Filter.eq('DIST_CODE', area_id))
            elif area_type == "protected_area":
                forest_featurecol = ee.FeatureCollection(GEEApi.GLAD_FOREST_ALERT_FC+""+str(year)+"/protected_Metadata")
                forest_alert = forest_featurecol.filter(ee.Filter.eq('map_id', area_id))

            areaHA = forest_alert.aggregate_array("areaHect").get(0).getInfo()

        return areaHA
    
    #-------------------------------------------------------------------------------------
    def getForestAlertArea(self, start_year, end_year):
        res = {}
        for _year in range(start_year, end_year+1):
            series_start = str(_year) + '-01-01'
            series_end = str(_year) + '-12-31'
            colorIndex += 1
            res[str(_year)] = self.calForestAlert(series_start, series_end, _year)
        return res

    # -------------------------------------------------------------------------
    def calSARAlert(self, series_start, series_end, year):
        if year == 2021:
            image = ee.Image('projects/cemis-camp/assets/sarAlert/alert_2021V4')
            image = image.select("landclass").clip(self.geometry).toInt16()
            binary_image = image.rename(['binary']).selfMask()

        elif year == 2022:
            image = ee.Image('projects/cemis-camp/assets/sarAlert/alert_2022V4')
            image = image.select("landclass").clip(self.geometry).toInt16()
            binary_image = image.rename(['binary']).selfMask()
        else: 
            SARIC = ee.ImageCollection(GEEApi.SAR_ALERT).filterBounds(self.geometry).filterDate(series_start, series_end)
            # image = ee.Image(GEEApi.SAR_ALERT+"/"+"alert_"+str(year))
            image = SARIC.sort('system:time_start', False).first()
            image = image.select("landclass").clip(self.geometry).toInt16()
            binary_image = image.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()
        
        #ee.Image.pixelArea()
        #multiply 900 (30m * 30m)
        reducer = binary_image.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer= ee.Reducer.sum(),
            geometry= self.geometry,
            crs = 'EPSG:32647', # WGS Zone N 47
            scale= 30,
            maxPixels= 1E20
        )
        #area in squre meter
        stats = reducer.getInfo()['binary']
        #convert to hactare divide by 10000
        areaHA = stats / 10000

        return areaHA
    
    # -------------------------------------------------------------------------
    def getSARAlertArea(self, start_year, end_year):
        res = {}
        for _year in range(start_year, end_year+1):
            series_start = str(_year) + '-01-01'
            series_end = str(_year) + '-12-31'
            colorIndex += 1
            res[str(_year)] = self.calSARAlert(series_start, series_end, _year)
        return res

    #================================= Fire Hotspot Monitoring =======================>
    #----------------------------------------------------------------------------------
    def getBurnedMap(self, year):
        #burned Area Feature collection
        ic = "projects/servir-mekong/Cambodia-Dashboard-tool/BurnArea/"+ area_type +"_"+ str(year) +"Metadata"
        burnedArea_fc = ee.FeatureCollection(ic)

        IC= GEEApi.FIRMS_BURNED_AREA.filterBounds(self.geometry).sort('system:time_start', False).filterDate(series_start, series_end)
        proj = ee.Projection('EPSG:4326')
        fire = IC.select('T21').max().toInt16().clip(self.geometry)

        #confidance more then 90%
        maskconf = IC.select('confidence').mean().gt(90).toInt16()
        fire = fire.updateMask(maskconf)
        fire = fire.reproject(crs=proj,scale=1000)
        #binary image
        image = fire.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()
        image = image.reproject(crs=proj,scale=1000)

        fireMap = self.getTileLayerUrl(image.visualize(min=0, max=1, palette=['red']))

        return fireMap

    # -------------------------------------------------------------------------
    def dowmloadFirmBurnedArea(self, year):
        #burned Area Feature collection
        series_start = str(year) + '-01-01'
        series_end = str(year) + '-12-31'
        IC= GEEApi.FIRMS_BURNED_AREA.filterBounds(self.geometry).sort('system:time_start', False).filterDate(series_start, series_end)
        proj = ee.Projection('EPSG:4326')
        fire = IC.select('T21').max().toInt16().clip(self.geometry)

        #confidance more then 90%
        maskconf = IC.select('confidence').mean().gt(90).toInt16()
        fire = fire.updateMask(maskconf)
        fire = fire.reproject(crs=proj,scale=1000)
        #binary image
        image = fire.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()
        image = image.reproject(crs=proj,scale=1000)

        try:
            dnldURL = image.getDownloadURL({
                    'name': 'BurnedArea'+year,
                    'scale': 1000,
                    'crs': 'EPSG:4326'
                })
            return {
                'downloadURL': dnldURL,
                'success': 'success'
                    }
        except Exception as e:
            return {
                'success': 'not success'
            }

    # -------------------------------------------------------------------------
    def calFirmBurnedArea(self, series_start, series_end, year):
        ic = "projects/servir-mekong/Cambodia-Dashboard-tool/BurnArea/"+ area_type +"_"+ str(year) +"Metadata"
        burnedArea_fc = ee.FeatureCollection(ic)

        IC= GEEApi.FIRMS_BURNED_AREA.filterBounds(self.geometry).sort('system:time_start', False).filterDate(series_start, series_end)
        proj = ee.Projection('EPSG:4326')
        fire = IC.select('T21').max().toInt16().clip(self.geometry)

        #confidance more then 90%
        maskconf = IC.select('confidence').mean().gt(90).toInt16()
        fire = fire.updateMask(maskconf)
        fire = fire.reproject(crs=proj,scale=1000)
        #binary image
        image = fire.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()
        image = image.reproject(crs=proj,scale=1000)

        if area_type == "draw" or area_type == "upload":

            v1 = image.addBands(image).reduceToVectors(
              crs= image.select('binary').projection(),
              scale= 1000,
              geometryType= 'polygon',
              eightConnected= False,
              labelProperty= 'zone',
              reducer= ee.Reducer.sum(),
              maxPixels= 1E15,
              bestEffort = True
            ).filterMetadata("sum","greater_than", 1)


            number_fire = v1.size().getInfo()
            #area in squre meter
            areaSq = number_fire * (1000*1000)
            #convert to hactare divide by 10000
            areaHA = areaSq / 10000

        else:
            if area_type == "country":
                ic = "projects/servir-mekong/Cambodia-Dashboard-tool/BurnArea/camMetadata"
                burnedArea_fc = ee.FeatureCollection(ic)
                burnedArea = burnedArea_fc.filter(ee.Filter.eq('NAME_ENGLI', area_id)).filter(ee.Filter.eq('year', year))
            elif area_type == "province":
                burnedArea = burnedArea_fc.filter(ee.Filter.eq('gid', area_id))
            elif area_type == "district":
                burnedArea = burnedArea_fc.filter(ee.Filter.eq('DIST_CODE', area_id))
            elif area_type == "protected_area":
                ic = "projects/servir-mekong/Cambodia-Dashboard-tool/BurnArea/protected_"+ str(year) +"Metadata"
                burnedArea_fc = ee.FeatureCollection(ic)
                burnedArea = burnedArea_fc.filter(ee.Filter.eq('map_id', area_id))

            areaHA = burnedArea.aggregate_array("areaHect").get(0).getInfo()
            number_fire = burnedArea.aggregate_array("numberFire").get(0).getInfo()
        
        return {
            'number_fire': int(number_fire),
            'total_area': float('%.2f' % areaHA)
        }
    # -------------------------------------------------------------------------
    def getBurnedArea(self, start_year, end_year):
        res = {}
        for _year in range(start_year, end_year+1):
            series_start = str(_year) + '-01-01'
            series_end = str(_year) + '-12-31'
            res[str(_year)] = self.calFirmBurnedArea(series_start, series_end, _year)
        return res




        

