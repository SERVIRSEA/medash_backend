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
    
    NDVI = settings.NDVI
    VHI = settings.VHI
    CWSI = settings.CWSI
    CDI = settings.CDI
    SPI3 = settings.SPI3
    SOIL_MOIST = settings.SOIL_MOIST
    RAINFALL = settings.RAINFALL
    SURF_TEMP = settings.SURF_TEMP
    REL_HUMID = settings.REL_HUMID

    COLOR = ['A8D9C6','B0DAB2','BFE1C9','AAD7A0','C3DE98','D5E59E','93D2BF','95CF9C','A4D7B8','9BD291','B1D78A','C9E08E','5CC199','77C78C','37B54A','126039','146232','0F8040','279445','449644','59A044','0E361E','236832','335024', '36461F']
    # COLORFORESTALERT = ['943126', 'B03A2E', 'CB4335', 'E74C3C', 'F1948A', 'F5B7B1','943126', 'B03A2E', 'CB4335', 'E74C3C', 'F1948A', 'F5B7B1']
    COLORFORESTALERT = [
        '#a31545', '#a31545', '#a31545', '#a31545', '#a31545', '#a31545',
        '#a31545', '#a31545', '#a31545', '#a31545', '#a31545', '#a31545'
    ]
    COLORSARALERT = ['fba004', 'f9bc16', 'ac9d0a', 'fba004', 'f9bc16', 'ac9d0a','fba004', 'f9bc16', 'ac9d0a','fba004', 'f9bc16', 'ac9d0a']

    geometry = ee.FeatureCollection(CAMBODIA_COUNTRY_BOUNDARY).geometry()

    SLD_NDVI = ['E85B3A', 'F99E59', 'FEC981', 'FFEDAB', 'F7FCDF', 'C4E687', '97D265', '58B453', '1A9641']
    SLD_CWSI = ['1A9641','58B453','97D265','C4E687','F7FCDF','FFEDAB','FEC981','F99E59','E85B3A']
    SLD_VHI = ['1A9641','58B453','97D265','C4E687','F7FCDF','FFEDAB','FEC981','F99E59','E85B3A']
    
    # Custom Raster style (SLD)
    SLD_CDI ="""
        <RasterSymbolizer>
            <ColorMap type="intervals" extended="false">
                <ColorMapEntry color="#88A541" quantity="0" label="Normal" />
                <ColorMapEntry color="#F89F1D" quantity="1" label="Watch" />
                <ColorMapEntry color="#B97A57" quantity="2" label="Warning" />
                <ColorMapEntry color="#880015" quantity="3" label="Alert" />
            </ColorMap>
        </RasterSymbolizer>
    """

    SLD_SPI3 = """
        <RasterSymbolizer>
            <ColorMap type="intervals" extended="false" >
                <ColorMapEntry color="#880015" quantity="-2.0" label="EXD (less than  -2.0)" />
                <ColorMapEntry color="#B97A57" quantity="-1.50" label="SED (-1.5 - -1.99)" />
                <ColorMapEntry color="#F89F1D" quantity="-1.0" label="MOD (-1.0 - -1.49)" />
                <ColorMapEntry color="#FFFFFF" quantity="10" label="Normal or Wet (gt -0.99)" />
            </ColorMap>
        </RasterSymbolizer>
    """

    SLD_SOIL_MOIST = """
        <RasterSymbolizer>
            <ColorMap type="intervals" extended="false" >
                <ColorMapEntry color="#880015" quantity="5" label="EXD (0 - 5)"/>
                <ColorMapEntry color="#B97A57" quantity="10" label="SED (6 - 10)" />
                <ColorMapEntry color="#F89F1D" quantity="20" label="MOD (11 - 20)" />
                <ColorMapEntry color="#FFFFFF" quantity="10000" label="Normal or Wet (gt 21)" />
            </ColorMap>
        </RasterSymbolizer>
    """

    SLD_SURF_TEMP = """
        <RasterSymbolizer>
            <ColorMap type="intervals" extended="false" >
                <ColorMapEntry color="#0370AF" quantity="15" label="0 - 10"/>
                <ColorMapEntry color="#348DBF" quantity="20" label="10 - 13" />
                <ColorMapEntry color="#75B4D4" quantity="21" label="13 - 16" />
                <ColorMapEntry color="#A5CEE2" quantity="22" label="16 - 19" />
                <ColorMapEntry color="#CDE2EC" quantity="23" label="19 - 22"/>
                <ColorMapEntry color="#F6F6F6" quantity="24" label="22 - 25" />
                <ColorMapEntry color="#F4D5C7" quantity="26" label="25 - 28" />
                <ColorMapEntry color="#F4B599" quantity="28" label="28 - 31" />
                <ColorMapEntry color="#EB846E" quantity="29" label="31 - 34"/>
                <ColorMapEntry color="#DA4247" quantity="30" label="34 - 36" />
                <ColorMapEntry color="#CA0020" quantity="100" label="36 +" />
            </ColorMap>
        </RasterSymbolizer>
    """

    SLD_RAINFALL = """
        <RasterSymbolizer>
            <ColorMap type="intervals" extended="false" >
                <ColorMapEntry color="#FFFFFF" quantity="1" label="0 - 1"/>
                <ColorMapEntry color="#E5B42C" quantity="2" label="1 - 2" />
                <ColorMapEntry color="#E3B022" quantity="3" label="2 - 3" />
                <ColorMapEntry color="#F2B464" quantity="4" label="3 - 4" />
                <ColorMapEntry color="#F2B464" quantity="5" label="4 - 5"/>
                <ColorMapEntry color="#F3E976" quantity="10" label="5 - 10" />
                <ColorMapEntry color="#91CE7E" quantity="20" label="10 - 20" />
                <ColorMapEntry color="#89CE74" quantity="30" label="20 - 30" />
                <ColorMapEntry color="#43BE87" quantity="40" label="30 - 40"/>
                <ColorMapEntry color="#34B485" quantity="50" label="40 - 50" />
                <ColorMapEntry color="#30B282" quantity="60" label="50 - 60" />
                <ColorMapEntry color="#069B42" quantity="70" label="60 - 70"/>
                <ColorMapEntry color="#069B42" quantity="100" label="70 +" />
            </ColorMap>
        </RasterSymbolizer>
    """

    SLD_REL_HUMID = """
        <RasterSymbolizer>
            <ColorMap type="intervals" extended="false" >
                <ColorMapEntry color="#7C3595" quantity="10" label="Less than 10"/>
                <ColorMapEntry color="#9B65AE" quantity="20" label="10 - 20" />
                <ColorMapEntry color="#BA98C9" quantity="30" label="20 - 30" />
                <ColorMapEntry color="#D4C1DD" quantity="40" label="30 - 40" />
                <ColorMapEntry color="#ECE5EF" quantity="50" label="40 - 50"/>
                <ColorMapEntry color="#E5F1E4" quantity="60" label="50 - 60" />
                <ColorMapEntry color="#C1E5BD" quantity="70" label="60 - 70" />
                <ColorMapEntry color="#95D295" quantity="80" label="70 - 80" />
                <ColorMapEntry color="#4AAD66" quantity="90" label="80 - 90"/>
                <ColorMapEntry color="#008837" quantity="100" label="90 +" />
            </ColorMap>
        </RasterSymbolizer>
    """

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
        # polygon area in Hectare
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
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv4/"+str(year)).clip(self.geometry)
        classNames = ['evergreen', 'semi-evergreen', 'deciduous', 'mangrove', 'flooded forest','rubber', 'other plantations', 'rice', 'cropland', 'surface water', 'grassland', 'woodshrub', 'built-up area', 'village', 'other']
        palette = ['267300', '38A800', '70A800', '00A884', 'B4D79E', 'AAFF00', 'F5F57A', 'FFFFBE', 'FFD37F', '004DA8', 'D7C29E', '89CD66', 'E600A9', 'A900E6', '6f6f6f']
        lcMap = self.getTileLayerUrl(lcImage.visualize(min=0, max=str(len(classNames)-1), palette=palette))
        return lcMap
    
    # -------------------------------------------------------------------------
    def getDownloadLandcoverMap(self, year):
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv4/"+str(year)).clip(self.geometry)
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
        except Exception as e:
            return {
                'success': 'not success'
            }

    # -------------------------------------------------------------------------
    def calLandcoverArea(self, series_start, series_end, year):
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv4/"+str(year)).clip(self.geometry)
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
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv4/"+str(year)).eq(7).clip(self.geometry).selfMask()
        palette = ['FFFFFF','FFFF00']
        lcRiceMap = self.getTileLayerUrl(lcImage.visualize(min=0, max=1, palette=palette))
        return lcRiceMap

    def downloadLandcoverRiceMap(self, year):
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv4/"+str(year)).eq(7).clip(self.geometry)
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
        try:
            rice_area = total_area["rice"]
        except (KeyError, TypeError):
            rice_area = 0
        return rice_area

    def getLandcoverRiceArea(self, start_year, end_year): 
        res = {}
        # print(end_year)
        start_year = int(start_year)
        end_year = int(end_year)

        if end_year >=2023:
            end_year = 2022
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
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv4/"+str(year)).eq(5).clip(self.geometry).selfMask()
        palette = ['FFFFFF','AAFF00']
        lcRubberMap = self.getTileLayerUrl(lcImage.visualize(min=0, max=1, palette=palette))
        return lcRubberMap

    def downloadLandcoverRubberMap(self, year):
        lcImage = ee.Image("projects/cemis-camp/assets/landcover/lcv4/"+str(year)).eq(5).clip(self.geometry)
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
        # rubber_area = total_area["rubber"]
        try:
            rubber_area = total_area["rubber"]
        except (KeyError, TypeError):
            rubber_area = 0
        return rubber_area

    def getLandcoverRubberArea(self, start_year, end_year): 
        res = {}
        start_year = int(start_year)
        end_year = int(end_year)

        if end_year >=2023:
            end_year = 2022
        else:
            end_year = end_year

        for year in range(start_year, end_year+1):
            series_start = str(year) + '-01-01'
            series_end = str(year) + '-12-31'
            res[str(year)] = self.calRubberTimeSeries(series_start, series_end, year)
        # print(res)
        return res
    
    def getLCBaselineMeasureArea(self, refLow, refHigh, studyLow, studyHigh, land_cover_type):
    
        def filter_and_merge(years, lcType):
            image_list = []
            for year in years:
                image = self.filter_landcover(year=year, lcType=lcType)
                image_list.append(image)
            return ee.ImageCollection(image_list).max()

        baseline_years = list(range(int(refLow), int(refHigh) + 1))
        measure_years = list(range(int(studyLow), int(studyHigh) + 1))

        baselineImage = filter_and_merge(baseline_years, land_cover_type)
        measureImage = filter_and_merge(measure_years, land_cover_type)

        baseline_area_stats = baselineImage.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=self.geometry,
            crs='EPSG:4326',
            scale=100,
            maxPixels=1E20
        )

        measure_area_stats = measureImage.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=self.geometry,
            crs='EPSG:4326',
            scale=100,
            maxPixels=1E20
        )

        baseline_area_Ha = baseline_area_stats.getInfo()[land_cover_type] / 10000
        measure_area_Ha = measure_area_stats.getInfo()[land_cover_type] / 10000

        return {
            'baselineArea': float('%.2f' % baseline_area_Ha),
            'measureArea': float('%.2f' % measure_area_Ha),
        }

    def filter_landcover(self, year, lcType):
        band_mapping = {'rice': 7, 'rubber': 5}

        band_number = band_mapping.get(lcType)
        
        if band_number is None:
            raise ValueError("Invalid land cover type")

        image = ee.Image("projects/cemis-camp/assets/landcover/lcv4/" + str(year)).clip(self.geometry)

        band_names = image.bandNames()
        if 'lc' in band_names.getInfo():
            image = image.select(['lc'], [lcType])
            selected_band_name = lcType
        elif 'classification' in band_names.getInfo():
            image = image.select(['classification'], [lcType])
            selected_band_name = lcType
        else:
            raise ValueError("No 'lc' or 'classification' band found in the image")

        selected_image = image.select([selected_band_name])
        masked_image = selected_image.eq(ee.Number(band_number)).selfMask()

        return masked_image

        
    #=============================== Forest Alert =======================>
    def getColorIndex(self, year):
        if year == 2018:
            colorIndex = 0
        elif year == 2019:
            colorIndex = 1
        elif year == 2020:
            colorIndex = 2
        elif year == 2021:
            colorIndex = 3
        elif year == 2022:
            colorIndex = 4
        elif year == 2023:
            colorIndex = 5
        return colorIndex
    #---------------------------------------------------------------------
    def getGLADAlertMap(self, year):
        year = int(year)
        series_start = str(year) + '-01-01'
        series_end = str(year) + '-12-31'
        GLADIC = ee.ImageCollection(GEEApi.GLAD_ALERT).filterBounds(self.geometry).filterDate(series_start, series_end)
        image = GLADIC.sort('system:time_start', False).first().select("alert").clip(self.geometry).toInt16()
        binary_image = image.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()
        colorIndex = self.getColorIndex(year)
        colorMap = GEEApi.COLORFORESTALERT[colorIndex]
        alertMap = self.getTileLayerUrl(binary_image.visualize(min=0, max=1, palette=colorMap))
        return alertMap
    
    #------------------------------------------------------------------------------------
    def getSARAlertMap(self, year):
        year = int(year)
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
        colorIndex = self.getColorIndex(year)
        colorMap = GEEApi.COLORSARALERT[colorIndex]
        sarAlertMap = self.getTileLayerUrl(binary_image.visualize(min=0, max=1, palette=colorMap))
        return sarAlertMap

    # -------------------------------------------------------------------------
    def downloadGLADAlertMap(self, year):
        series_start = str(year) + '-01-01'
        series_end = str(year) + '-12-31'
        GLADIC = ee.ImageCollection(GEEApi.GLAD_ALERT).filterBounds(self.geometry).filterDate(series_start, series_end)
        image = GLADIC.sort('system:time_start', False).first().select("alert").clip(self.geometry).toInt16()
        binary_image = image.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()

        try:
            dnldURL = binary_image.getDownloadURL({
                    'name': 'GLADAlert'+year,
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
    def downloadSARAlertMap(self, year):
        year = int(year)
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
        
        try:
            dnldURL = binary_image.getDownloadURL({
                    'name': 'SARAlert'+str(year),
                    'scale': 100,
                    'crs': 'EPSG:4326'
                })
            return {
                'downloadURL': dnldURL,
                'success': 'success'
                }
        except Exception as e:
            print(e)
            return {
                'success': 'not success'
            }

    #-------------------------------------------------------------------------
    def calGLADAlert(self, series_start, series_end, year, area_type, area_id): 
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
                forest_alert = forest_featurecol.filter(ee.Filter.eq('gid', int(area_id)))
            elif area_type == "district":
                forest_featurecol = ee.FeatureCollection(GEEApi.GLAD_FOREST_ALERT_FC+""+str(year)+"/district_Metadata")
                forest_alert = forest_featurecol.filter(ee.Filter.eq('DIST_CODE', str(area_id)))
            elif area_type == "protected_area":
                forest_featurecol = ee.FeatureCollection(GEEApi.GLAD_FOREST_ALERT_FC+""+str(year)+"/protected_Metadata")
                forest_alert = forest_featurecol.filter(ee.Filter.eq('map_id', str(area_id)))

            areaHA = forest_alert.aggregate_array("areaHect").get(0).getInfo()

        return areaHA
    
    #-------------------------------------------------------------------------------------
    def getGLADAlertArea(self, start_year, end_year, area_type, area_id):
        res = {}
        for _year in range(int(start_year), int(end_year)+1):
            series_start = str(_year) + '-01-01'
            series_end = str(_year) + '-12-31'
            res[str(_year)] = self.calGLADAlert(series_start, series_end, _year, area_type, area_id)
        return res

    # -------------------------------------------------------------------------
    def calSARAlert(self, series_start, series_end, year):
        try:
            if year == 2021:
                image = ee.Image('projects/cemis-camp/assets/sarAlert/alert_2021V4')
            elif year == 2022:
                image = ee.Image('projects/cemis-camp/assets/sarAlert/alert_2022V4')
            else:
                SARIC = ee.ImageCollection(GEEApi.SAR_ALERT).filterBounds(self.geometry).filterDate(series_start, series_end)
                image = SARIC.sort('system:time_start', False).first()

            # Ensure that the "landclass" band exists in the image
            if "landclass" not in image.bandNames().getInfo():
                raise ValueError("The 'landclass' band is not available in the selected image.")

            # Select the 'landclass' band
            landclass_image = image.select("landclass").clip(self.geometry).toInt16()

            # Create a binary image based on the selected landclass
            binary_image = landclass_image.neq(0).rename(['binary']).multiply(1).toInt16().selfMask()

            # Compute area in square meters
            reducer = binary_image.multiply(ee.Image.pixelArea()).reduceRegion(
                reducer=ee.Reducer.sum(),
                geometry=self.geometry,
                crs='EPSG:32647',  # WGS Zone N 47
                scale=30,
                maxPixels=1E20
            )

            # Get the area in square meters
            stats = reducer.getInfo()['binary'] if reducer.getInfo().get('binary') is not None else 0

            # Convert to hectares (divide by 10000)
            areaHA = stats / 10000

            return areaHA

        except Exception as e:
            # Handle exceptions (e.g., missing bands, invalid images)
            return 0
    
    # -------------------------------------------------------------------------
    def getSARAlertArea(self, start_year, end_year):
        res = {}
        for _year in range(int(start_year), int(end_year)+1):
            series_start = str(_year) + '-01-01'
            series_end = str(_year) + '-12-31'
            res[str(_year)] = self.calSARAlert(series_start, series_end, _year)
        return res
    
    #================================= Forest Monitoring =============================>
    # -------------------------------------------------------------------------
    def tree_canopy(self, 
        img_coll = None, 
        get_image = False,
        for_download = False,
        year = None,
        tree_canopy_definition = 10,
        ):

        if not year:
            return {
                'message': 'Please specify a year for which you want to perform the calculations!'
            }

        if not img_coll:
            def _apply_tree_canopy_definition(img):
                mask = img.select(0).gt(tree_canopy_definition)
                return img.updateMask(mask).rename(['tcc'])

            img_coll = GEEApi.TREE_CANOPY
            img_coll = img_coll.map(_apply_tree_canopy_definition)

        image = ee.Image(img_coll.filterDate('%s-01-01' % year,
                                             '%s-12-31' % year).first())

        if get_image:
            if for_download:
                return image.updateMask(image).clip(self.geometry)
            else:
                return image.clip(self.geometry)

        image = image.updateMask(image).clip(self.geometry)

        map_id = image.getMapId({
            'min': str(tree_canopy_definition),
            'max': '100',
            'palette': 'f7fcf5,e8f6e3,d0edca,b2e0ab,8ed18c,66bd6f,3da75a,238c45,03702e,00441b'
        })

        return {
            'eeMapId': str(map_id['mapid']),
            'eeMapURL': str(map_id['tile_fetcher'].url_format)
        }

    # -------------------------------------------------------------------------
    def tree_height(self, 
        img_coll = None,
        get_image = False,
        for_download = False,
        year = None,
        tree_height_definition = 5,
        ):

        if not year:
            return {
                'message': 'Please specify a year for which you want to perform the calculations!'
            }

        if not img_coll:
            def _apply_tree_height_definition(img):
                mask = img.select(0).gt(tree_height_definition)
                return img.updateMask(mask)

            img_coll = GEEApi.TREE_HEIGHT
            img_coll = img_coll.map(_apply_tree_height_definition)

        image = ee.Image(img_coll.filterDate('%s-01-01' % year,
                                             '%s-12-31' % year).mean())

        if get_image:
            if for_download:
                return image.updateMask(image).clip(self.geometry)
            else:
                return image.clip(self.geometry)

        image = image.updateMask(image).clip(self.geometry)

        map_id = image.getMapId({
            'min': str(tree_height_definition),
            'max': '36', #'{}'.format(int(math.ceil(max.getInfo()[max.getInfo().keys()[0]]))),
            #'palette': 'f7fcf5,e8f6e3,d0edca,b2e0ab,8ed18c,66bd6f,3da75a,238c45,03702e,00441b'
            'palette': '410f74,5e177f,7b2282,982c80,b63679,d3426e,eb5761,f8765c,fe9969,febb80,fedc9d,fcfdbf'
        })

        return {
            'eeMapId': str(map_id['mapid']),
            'eeMapURL': str(map_id['tile_fetcher'].url_format)
        }

    # -------------------------------------------------------------------------
    @staticmethod
    def _get_combined_img_coll(end_year):
        years = ee.List.sequence(2000, end_year)
        date_ymd = ee.Date.fromYMD

        def addBands(_year):
            tcc = GEEApi.TREE_CANOPY.filterDate(date_ymd(_year, 1, 1),
                                                       date_ymd(_year, 12, 31)).first()
            
            tcc = ee.Image(tcc).rename(['tcc'])
            tch = GEEApi.TREE_HEIGHT.filterDate(date_ymd(_year, 1, 1),
                                                       date_ymd(_year, 12, 31)).first()

            tch = ee.Image(tch).rename(['tch'])

            return ee.Image(tcc).addBands(tch)

        ic = ee.ImageCollection.fromImages(years.map(addBands))
        return ic

    # -------------------------------------------------------------------------
    @staticmethod
    def _filter_for_forest_definition(img_coll,
                                      tree_canopy_definition,
                                      tree_height_definition):

        # 0 - tcc
        # 1 - tch
        return img_coll.map(lambda img: img.select('tcc').gt(tree_canopy_definition).\
                            And(img.select('tch').gt(tree_height_definition))
                            .rename(['forest_cover']).copyProperties(img, img.propertyNames()))

    # -------------------------------------------------------------------------
    def getForestGainMap(self,
        get_image = False,
        studyLow = None,
        studyHigh = None,
        tree_canopy_definition = 10,
        tree_height_definition = 5,
        download = 'False'):

        start_year = int(studyLow)
        end_year = int(studyHigh)

        if not studyLow or not studyHigh:
            return {
                'message': 'Please specify a start and end year for which you want to perform the calculations!'
            }

        combined_img_coll = GEEApi._get_combined_img_coll(end_year)

        filtered_img_coll = GEEApi._filter_for_forest_definition(\
                                                        combined_img_coll,
                                                        tree_canopy_definition,
                                                        tree_height_definition)

        start_image = self.tree_canopy(img_coll = filtered_img_coll,
                                       get_image = True,
                                       year = start_year,
                                       tree_canopy_definition = tree_canopy_definition,
                                       )

        end_image = self.tree_canopy(img_coll = filtered_img_coll,
                                     get_image = True,
                                     year = end_year,
                                     tree_canopy_definition = tree_canopy_definition,
                                     )

        gain_image = end_image.subtract(start_image).gt(0)
        gain_image = gain_image.updateMask(gain_image).select('forest_cover').clip(self.geometry)
        
        # print(gain_image.getInfo())
        if download == 'True':
            try:
                dnldURL = gain_image.getDownloadURL({
                    'name': 'ForestGain'+str(start_year)+'_'+str(end_year),
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
        if get_image:
            return gain_image
        else:
            forestGainMap = self.getTileLayerUrl(gain_image.visualize(min=0, max=100, palette=['173F5F']))
            return forestGainMap

    # -------------------------------------------------------------------------
    def getForestLossMap(self,
        get_image = False,
        studyLow = None,
        studyHigh = None,
        tree_canopy_definition = 10,
        tree_height_definition = 5,
        download = 'False'):

        start_year = int(studyLow)
        end_year = int(studyHigh)
        
        if not start_year and end_year:
            return {
                'message': 'Please specify a start and end year for which you want to perform the calculations!'
            }

        combined_img_coll = GEEApi._get_combined_img_coll(end_year)

        filtered_img_coll = GEEApi._filter_for_forest_definition(\
                                                        combined_img_coll,
                                                        tree_canopy_definition,
                                                        tree_height_definition)

        start_image = self.tree_canopy(img_coll = filtered_img_coll,
                                       get_image = True,
                                       year = start_year,
                                       tree_canopy_definition = tree_canopy_definition,
                                       )

        end_image = self.tree_canopy(img_coll = filtered_img_coll,
                                     get_image = True,
                                     year = end_year,
                                     tree_canopy_definition = tree_canopy_definition,
                                     )

        loss_image = end_image.subtract(start_image).lt(0)
        loss_image = loss_image.updateMask(loss_image).select('forest_cover').clip(self.geometry)

        if download == 'True':
            try:
                dnldURL = loss_image.getDownloadURL({
                    'name': 'ForestLoss'+str(start_year)+'_'+str(end_year),
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
        
        if get_image:
            return loss_image
        else:
            forestLossMap = self.getTileLayerUrl(loss_image.visualize(min=0, max=1, palette=['fdb827']))
            return forestLossMap

    def forest_extend(self,
        get_image = False,
        year = None,
        tree_canopy_definition = 10,
        tree_height_definition = 5,
        start_year = 2000,
        end_year=None,
        area_type='',
        area_id='',
        download='False'):

        if not year:
            return {
                'message': 'Please specify a year for which you want to perform the calculations!'
            }

        combined_img_coll = GEEApi._get_combined_img_coll(end_year)

        filtered_img_coll = GEEApi._filter_for_forest_definition(\
                                                        combined_img_coll,
                                                        tree_canopy_definition,
                                                        tree_height_definition)

        image = self.tree_canopy(img_coll = filtered_img_coll,
                                 get_image = True,
                                 year = year,
                                 tree_canopy_definition = tree_canopy_definition,
                                 )

        image = image.updateMask(image).clip(self.geometry)

        # map_id = image.getMapId({
        #     'min': str(tree_canopy_definition),
        #     'max': '100',
        #     'palette': GEEApi.COLOR[year - start_year]
        # })

        if area_type == "country":
            ic = "projects/servir-mekong/Cambodia-Dashboard-tool/ForestArea/cam_Metadata"
            forestArea_fc = ee.FeatureCollection(ic)
            forestArea = forestArea_fc.filter(ee.Filter.eq('NAME_ENGLI', area_id)).filter(ee.Filter.eq('year', year))
            areaHA = forestArea.aggregate_array("areaHect").get(0).getInfo()

        elif area_type == "province":
            ic = "projects/servir-mekong/Cambodia-Dashboard-tool/ForestArea/province_"+ str(year) +"Metadata"
            forestArea_fc = ee.FeatureCollection(ic)
            forestArea = forestArea_fc.filter(ee.Filter.eq('gid', int(area_id)))
            areaHA = forestArea.aggregate_array("areaHect").get(0).getInfo()

        elif area_type == "district":
            ic = "projects/servir-mekong/Cambodia-Dashboard-tool/ForestArea/district_"+ str(year) +"Metadata"
            forestArea_fc = ee.FeatureCollection(ic)
            forestArea = forestArea_fc.filter(ee.Filter.eq('DIST_CODE', str(area_id)))
            areaHA = forestArea.aggregate_array("areaHect").get(0).getInfo()

        elif area_type == "protected_area":
            ic = "projects/servir-mekong/Cambodia-Dashboard-tool/ForestArea/protected_"+ str(year) +"Metadata"
            forestArea_fc = ee.FeatureCollection(ic)
            forestArea = forestArea_fc.filter(ee.Filter.eq('map_id', str(area_id)))
            areaHA = forestArea.aggregate_array("areaHect").get(0).getInfo()

        elif area_type == "draw" or area_type == "upload":
            reducer = image.gt(0).multiply(self.scale).multiply(self.scale).reduceRegion(
                reducer = ee.Reducer.sum(),
                geometry = self.geometry,
                crs = 'EPSG:32647', # WGS Zone N 47
                scale = self.scale,
                maxPixels = 10**15
            )
            stats = reducer.getInfo()["forest_cover"]
            # in hectare
            areaHA = stats * 0.0001
        
        if download == 'True':
            try:
                dnldURL = image.getDownloadURL({
                    'name': 'forest'+str(year),
                    'scale': 100,
                    'crs': 'EPSG:4326'
                })
                return {
                    'downloadURL': dnldURL,
                    'success': 'success'
                        }
            except Exception as e:
                print(e)
                return {
                    'success': 'not success'
                }

        if get_image:
            data = self.getTileLayerUrl(
                image.visualize(
                    min=str(tree_canopy_definition), 
                    max='100', 
                    palette=[GEEApi.COLOR[year - start_year]]))
            return data
        else:
            
            return {
                'forest': float('%.2f' % areaHA),
                'noneForest': float('%.2f' % (self.geometryArea - areaHA)),
            }
        

    # -------------------------------------------------------------------------
    def getForestExtendMap(self, studyLow, studyHigh, tree_canopy_definition, tree_height_definition, area_type, area_id, year=None, download="False"):
        start_year = int(studyLow)
        end_year = int(studyHigh)

        if download == "True":
            res = self.forest_extend(get_image = False,
                                       year = year,
                                       tree_canopy_definition = tree_canopy_definition,
                                       tree_height_definition = tree_height_definition,
                                       start_year = start_year,
                                       end_year= end_year,
                                       area_type= area_type, 
                                       area_id=area_id,
                                       download="True")
            return res

        
        else:
            res = {}
            for _year in range(start_year, end_year+1):
                res[str(_year)] = self.forest_extend(get_image = True,
                                        year = _year,
                                        tree_canopy_definition = tree_canopy_definition,
                                        tree_height_definition = tree_height_definition,
                                        start_year = start_year,
                                        end_year= end_year,
                                        area_type= area_type, area_id=area_id)

            try:
                return res
            except Exception as e:
                return {
                    'reportError': e.message
                }

    def getForestNonForestArea(self, studyLow, studyHigh, tree_canopy_definition, tree_height_definition, area_type, area_id):
        start_year = int(studyLow)
        end_year = int(studyHigh)
        res = {}
        for _year in range(start_year, end_year+1):
            res[str(_year)] = self.forest_extend(get_image = False,
                year = _year,
                tree_canopy_definition = tree_canopy_definition,
                tree_height_definition = tree_height_definition,
                start_year = start_year,
                end_year= end_year,
                area_type= area_type, area_id=area_id)

        try:
            return res
        except Exception as e:
            return {
                'reportError': e.message
            }

    # -------------------------------------------------------------------------
    def getForestGainLossArea(self, studyLow, studyHigh, tree_canopy_definition, tree_height_definition):
        res = {}
        name = 'forest_cover'
        start_year = int(studyLow)
        end_year = int(studyHigh)
        imageLoss = self.getForestLossMap(get_image = True,
                                    studyLow = start_year,
                                    studyHigh = end_year,
                                    tree_canopy_definition = tree_canopy_definition,
                                    tree_height_definition = tree_canopy_definition,
                                    )
        imageGain = self.getForestGainMap(get_image = True,
                                    studyLow = start_year,
                                    studyHigh = end_year,
                                    tree_canopy_definition = tree_canopy_definition,
                                    tree_height_definition = tree_height_definition
                                    )

        reducerLoss = imageLoss.gt(0).multiply(self.scale).multiply(self.scale).reduceRegion(
            reducer = ee.Reducer.sum(),
            geometry = self.geometry,
            crs = 'EPSG:32647', # WGS Zone N 47
            scale = self.scale,
            maxPixels = 10**15
        )
        reducerGain = imageGain.gt(0).multiply(self.scale).multiply(self.scale).reduceRegion(
            reducer = ee.Reducer.sum(),
            geometry = self.geometry,
            crs = 'EPSG:32647', # WGS Zone N 47
            scale = self.scale,
            maxPixels = 10**15
        )

        statsLoss = reducerLoss.getInfo()[name]
        statsGain = reducerGain.getInfo()[name]
        # in hectare
        statsLoss = statsLoss * 0.0001
        statsGain = statsGain * 0.0001

        res['forestgain'] = float('%.2f' % statsGain)
        res['forestloss'] = float('%.2f' % statsLoss)

        return res
    
    # -------------------------------------------------------------------------
    def getForestChangeGainLoss(self, studyLow, studyHigh, refLow, refHigh, tree_canopy_definition, tree_height_definition):
        res = {}
        name = 'forest_cover'
        refLoss = self.getForestLossMap(get_image = True,
                                 studyLow = refLow,
                                 studyHigh = refHigh,
                                 tree_canopy_definition = tree_canopy_definition,
                                 tree_height_definition = tree_canopy_definition,
                                 )
        studyLoss = self.getForestLossMap(get_image = True,
                                 studyLow = studyLow,
                                 studyHigh = studyHigh,
                                 tree_canopy_definition = tree_canopy_definition,
                                 tree_height_definition = tree_canopy_definition,
                                 )

        refGain = self.getForestGainMap(get_image = True,
                                 studyLow = refLow,
                                 studyHigh = refHigh,
                                 tree_canopy_definition = tree_canopy_definition,
                                 tree_height_definition = tree_height_definition
                                 )

        studyGain = self.getForestGainMap(get_image = True,
                                 studyLow = studyLow,
                                 studyHigh = studyHigh,
                                 tree_canopy_definition = tree_canopy_definition,
                                 tree_height_definition = tree_height_definition
                                 )

        reducerRefLoss = refLoss.gt(0).multiply(ee.Image.pixelArea()).reduceRegion(
            reducer = ee.Reducer.sum(),
            geometry = self.geometry,
            crs = 'EPSG:32647', # WGS Zone N 47
            scale = self.scale,
            maxPixels = 10**15
        )
        reducerStudyLoss = studyLoss.gt(0).multiply(ee.Image.pixelArea()).reduceRegion(
            reducer = ee.Reducer.sum(),
            geometry = self.geometry,
            crs = 'EPSG:32647', # WGS Zone N 47
            scale = self.scale,
            maxPixels = 10**15
        )
        reducerRefGain = refGain.gt(0).multiply(ee.Image.pixelArea()).reduceRegion(
            reducer = ee.Reducer.sum(),
            geometry = self.geometry,
            crs = 'EPSG:32647', # WGS Zone N 47
            scale = self.scale,
            maxPixels = 10**15
        )
        reducerStudyGain = studyGain.gt(0).multiply(ee.Image.pixelArea()).reduceRegion(
            reducer = ee.Reducer.sum(),
            geometry = self.geometry,
            crs = 'EPSG:32647', # WGS Zone N 47
            scale = self.scale,
            maxPixels = 10**15
        )

        statsRefLoss = reducerRefLoss.getInfo()[name]
        statsStudyLoss = reducerStudyLoss.getInfo()[name]
        statsRefGain = reducerRefGain.getInfo()[name]
        statsStudyGain = reducerStudyGain.getInfo()[name]

        # in hectare
        statsRefLoss = statsRefLoss * 0.0001
        statsStydyLoss = statsStudyLoss * 0.0001
        statsRefGain = statsRefGain * 0.0001
        statsStudyGain = statsStudyGain * 0.0001

        res['statsRefLoss'] = float('%.2f' % statsRefLoss)
        res['statsStudyLoss'] = float('%.2f' % statsStydyLoss)
        res['statsRefGain'] = float('%.2f' % statsRefGain)
        res['statsStudyGain'] = float('%.2f' % statsStudyGain)

        return res

    #================================= Fire Hotspot Monitoring =======================>
    #----------------------------------------------------------------------------------
    def getBurnedMap(self, year, area_type):
        #burned Area Feature collection
        ic = "projects/servir-mekong/Cambodia-Dashboard-tool/BurnArea/"+ area_type +"_"+ str(year) +"Metadata"
        burnedArea_fc = ee.FeatureCollection(ic)
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

        fireMap = self.getTileLayerUrl(image.visualize(min=0, max=1, palette=['red']))

        return fireMap

    # -------------------------------------------------------------------------
    def downloadFirmBurnedArea(self, year):
        # burned Area Feature collection
        series_start = str(year) + '-01-01'
        series_end = str(year) + '-12-31'
        IC= GEEApi.FIRMS_BURNED_AREA.filterBounds(self.geometry).sort('system:time_start', False).filterDate(series_start, series_end)
        proj = ee.Projection('EPSG:4326')
        fire = IC.select('T21').max().toInt16().clip(self.geometry)

        # confidance more then 90%
        maskconf = IC.select('confidence').mean().gt(90).toInt16()
        fire = fire.updateMask(maskconf)
        fire = fire.reproject(crs=proj,scale=1000)
        # binary image
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
    def calFirmBurnedArea(self, series_start, series_end, year, area_type, area_id):
        # ic = "projects/servir-mekong/Cambodia-Dashboard-tool/BurnArea/"+ area_type +"_"+ str(year) +"Metadata"
        # burnedArea_fc = ee.FeatureCollection(ic)

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
                ic = "projects/servir-mekong/Cambodia-Dashboard-tool/BurnArea/province_"+ str(year) +"Metadata"
                burnedArea_fc = ee.FeatureCollection(ic)
                # print(area_id)
                burnedArea = burnedArea_fc.filter(ee.Filter.eq('gid', int(area_id)))
                # print(burnedArea)
            elif area_type == "district":
                ic = "projects/servir-mekong/Cambodia-Dashboard-tool/BurnArea/district_"+ str(year) +"Metadata"
                burnedArea_fc = ee.FeatureCollection(ic)
                burnedArea = burnedArea_fc.filter(ee.Filter.eq('DIST_CODE', str(area_id)))
            elif area_type == "protected_area":
                ic = "projects/servir-mekong/Cambodia-Dashboard-tool/BurnArea/protected_"+ str(year) +"Metadata"
                burnedArea_fc = ee.FeatureCollection(ic)
                burnedArea = burnedArea_fc.filter(ee.Filter.eq('map_id', str(area_id)))
            
            # Get the list of areaHect values
            areaHA_list = burnedArea.aggregate_array("areaHect").getInfo()
            # print(areaHA_list)
            # Check if the list is not empty before accessing elements
            if areaHA_list:
                areaHA = areaHA_list[0]
            else:
                # Handle the case where the list is empty
                areaHA = 0  # Or any default value

            # Similarly, handle numberFire
            number_fire_list = burnedArea.aggregate_array("numberFire").getInfo()
            if number_fire_list:
                number_fire = number_fire_list[0]
            else:
                number_fire = 0  # Or any default value
            # areaHA = burnedArea.aggregate_array("areaHect").get(0).getInfo()
            # number_fire = burnedArea.aggregate_array("numberFire").get(0).getInfo()
        
        return {
            'number_fire': int(number_fire),
            'total_area': float('%.2f' % areaHA)
        }
    # -------------------------------------------------------------------------
    def getBurnedArea(self, start_year, end_year, area_type, area_id):
        res = {}
        for _year in range(int(start_year), int(end_year)+1):
            series_start = str(_year) + '-01-01'
            series_end = str(_year) + '-12-31'
            res[str(_year)] = self.calFirmBurnedArea(series_start, series_end, _year, area_type, area_id)
        return res

    # ========= Drought section =======>
    def getVisualizationParams(self, index):
        params_dict = {
            'ndvi': {'min': -10000, 'max': 10000, 'palette': GEEApi.SLD_NDVI, 'sld': False, 'band': 'NDVI'},
            'vhi': {'min': 0, 'max': 10000, 'palette': GEEApi.SLD_VHI, 'sld': False, 'band': 'VHI'},
            'cwsi': {'min': 0, 'max': 1, 'palette': GEEApi.SLD_CWSI, 'sld': False, 'band': 'CWSI'},
            'cdi': {'min': 0, 'max': 10, 'palette': GEEApi.SLD_CDI, 'sld': True, 'band': 'cdi'},
            'spi3': {'min': -10, 'max': 10, 'palette': GEEApi.SLD_SPI3, 'sld': True, 'band': 'b1'},
            'soil_moist': {'min': 0, 'max': 100, 'palette': GEEApi.SLD_SOIL_MOIST, 'sld': True, 'band': 'b1'},
            'rainfall': {'min': 0, 'max': 100, 'palette': GEEApi.SLD_RAINFALL, 'sld': True, 'band': 'b1'},
            'surf_temp': {'min': 0, 'max': 100, 'palette': GEEApi.SLD_SURF_TEMP, 'sld': True, 'band': 'b1'},
            'rel_humid': {'min': 0, 'max': 100, 'palette': GEEApi.SLD_REL_HUMID, 'sld': True, 'band': 'b1'}
        }
        return params_dict.get(index.lower(), {})

    def getDroughtIndexMap(self, index, date):
        image_collection_path = getattr(GEEApi, index.upper())
        
        image_collection = (
            ee.ImageCollection(image_collection_path)
            .filterBounds(self.geometry)
            # .sort('system:time_start', False)
        )

        if index == 'vhi':
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            # Format the datetime object to 'YYYY_MM_dd'
            formatted_date = date_obj.strftime('%Y_%m_%d')
            vhi_filter = ee.Filter.eq('system:index', f'vhi_{formatted_date}')
            image_collection = image_collection.filter(vhi_filter)
        else:
            date = ee.Date(date)
            filter = ee.Filter.date(date, date.advance(1, 'day'))
            image_collection = image_collection.filter(filter)

        image = image_collection.first().clip(self.geometry)
        vis_params = self.getVisualizationParams(index)
        band_name = vis_params.get('band', 'NDVI')
        sld =  vis_params.get('sld')
        image = image.select(band_name)
        image = image.selfMask()
        imgScale = image.projection().nominalScale()
        image = image.reproject(crs='EPSG:4326', scale=imgScale)

        if sld == True:
            style = vis_params['palette']
            map_id = image.sldStyle(style).getMapId()
            indexMap = str(map_id['tile_fetcher'].url_format)
        else:
            indexMap = self.getTileLayerUrl(image.visualize(min=vis_params['min'], max=vis_params['max'], palette=vis_params['palette']))
        
        return indexMap