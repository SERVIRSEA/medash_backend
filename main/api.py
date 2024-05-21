import os, json
import orjson
from django.shortcuts import render
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .core import GEEApi
from .dbcore import DBData
from .download_link import DownloadLink
from .authentication import APIKeyAuthentication
from .models import DownloadRequest

@csrf_exempt 
@api_view(['GET', 'POST'])
@authentication_classes([APIKeyAuthentication])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def api(request):
    # action = request.query_params.get('action', '')
    action = request.query_params.get('action', '') if request.method == 'GET' else request.data.get('action', '')
    
    if action:
        request_methods = [
            'get-evi-map',
            'get-evi-pie',
            'get-evi-line',
            'get-landcover-map',
            'get-landcover-chart',
            'get-landcover-rice-map', 
            'get-landcover-rubber-map',
            'get-landcover-rice-line-data',
            'get-landcover-rubber-line-data',
            'get-forest-gain-map',
            'get-forest-loss-map',
            'get-forest-extent-map',
            'get-forest-nonforest-chart-data',
            'get-forest-gainloss-area',
            'get-forest-change-gainloss-chart-data',
            'get-glad-alert-map',
            'get-sar-alert-map',
            'get-glad-alert-chart-data',
            'get-sar-alert-chart-data',
            'get-burned-area',
            'get-burned-area-chart-data',
            'get-drought-index-map',
            'get-drought-index-dates',
            'get-weather-map',
            'get-landcover-baselinemeasure-area',
            'download-evi-map',
            'download-landcover-map',
            'download-landcover-rice-map',
            'download-landcover-rubber-map',
            'download-burned-area-map',
            'download-gladalert-map',
            'download-saralert-map',
            'download-forest-gain-map',
            'download-forest-loss-map',
            'download-forest-extent-map',
            'download-drought-index-map',
            'download-weather-map',
            'get-glad-deforestation-alert-map',
            'get-combined-deforestation-alert-map',
            'get-doy-glad-deforestation-alert-map',
            'download-glad-deforestation-alert-map',
            'download-combined-deforestation-alert-map',
            'download-doy-glad-deforestation-alert-map',
            'get-sar-biweekly-alert',
            'download-sar-biweekly-alert',
            'get-forestchange-chart',
            'post-download-form-data'    
        ]

        if action in request_methods:
            if request.method == 'GET':
                area_type = request.query_params.get('area_type', '')
                area_id = request.query_params.get('area_id', '')
                refLow = request.query_params.get('refLow', '')
                refHigh = request.query_params.get('refHigh', '')
                studyLow = request.query_params.get('studyLow', '')
                studyHigh = request.query_params.get('studyHigh', '')
                year = request.query_params.get('year', '') 
                index = request.query_params.get('index', '')
                date = request.query_params.get('date', '')
                land_cover_type =  request.query_params.get('type', '')
                weather_param = request.query_params.get('weather_param', '')
                weather_type = request.query_params.get('weather_type', '')
                start_date = request.query_params.get('start_date', '')
                end_date = request.query_params.get('end_date', '')
                doy = request.query_params.get('doy', '')
            elif request.method == 'POST':
                name = request.data.get('name', '')
                email = request.data.get('email', '')
                institution = request.data.get('institution', '')
                job_title = request.data.get('jobTitle', '')
                dataset = request.data.get('dataset', '')
                purpose_of_download = request.data.get('purposeOfDownload', '')
                area_type = request.data.get('area_type', '')
                area_id = request.data.get('area_id', '')
                refLow = request.data.get('refLow', '')
                refHigh = request.data.get('refHigh', '')
                studyLow = request.data.get('studyLow', '')
                studyHigh = request.data.get('studyHigh', '')
                year = request.data.get('year', '') 
                date = request.data.get('date', '')
                index = request.data.get('index', '') 
                weather_param = request.data.get('weather_param', '')
                weather_type = request.data.get('weather_type', '')
            else:
                pass
            
            core = GEEApi(area_type, area_id)
            dbcore = DBData(area_type, area_id)
            dlink = DownloadLink()

            tree_canopy_definition = 10
            tree_height_definition = 5 

            # Form data
            if action == 'post-download-form-data':
                try:
                    # Save the form data to the database
                    download_request = DownloadRequest(
                        name=name,
                        email=email,
                        institution=institution,
                        job_title=job_title,
                        dataset=dataset,
                        purpose_of_download=purpose_of_download
                    )
                    download_request.save()

                    # Initialize download_link to None or some default value
                    download_link = None

                    if dataset == 'Landcover':
                        download_link = dlink.get_download_link_lc(year)
                    elif dataset == 'EVI':
                        data = core.getDownloadEVIMap(refLow, refHigh, studyLow, studyHigh)
                        if data['success'] == 'success':
                            download_link = data['downloadURL']
                    elif dataset == 'Forestcover':
                        download_link = dlink.get_download_link_forestcover(year)
                    elif dataset == 'Rice':
                        download_link = dlink.get_download_link_rice(year)
                    elif dataset == 'Rubber':
                        download_link = dlink.get_download_link_rubber(year)
                    elif dataset == 'ForestGain':
                        data = core.getForestGainMap(False, str(studyLow), str(studyHigh), tree_canopy_definition, tree_height_definition, download='True')
                        if data['success'] == 'success':
                            download_link = data['downloadURL']
                    elif dataset == 'ForestLoss':
                        data = core.getForestLossMap(False, str(studyLow), str(studyHigh), tree_canopy_definition, tree_height_definition, download='True')
                        if data['success'] == 'success':
                            download_link = data['downloadURL']
                    elif dataset == 'FireHotspot':
                        data = core.downloadFirmBurnedArea(str(year))
                        if data['success'] == 'success':
                            download_link = data['downloadURL']
                    elif dataset == 'SARAlert':
                        data = core.downloadSARAlertMap(str(year))
                        if data['success'] == 'success':
                            download_link = data['downloadURL']
                    elif dataset == 'GLADAlert':
                        data = core.downloadGLADAlertMap(str(year))
                        if data['success'] == 'success':
                            download_link = data['downloadURL']
                    elif dataset == 'Drought':
                        data = core.downloadDroughtIndexMap(index, date)
                        if data['success'] == 'success':
                            download_link = data['downloadURL']
                    elif dataset == 'ShortTermWeather':
                        data = core.get_weather_map(weather_param, weather_type, download="True")
                        if data['success'] == 'success':
                            download_link = data['downloadURL']
                    elif dataset == 'LongTermWeather':
                        data = core.get_weather_map(weather_param, weather_type, download="True")
                        if data['success'] == 'success':
                            download_link = data['downloadURL']
                    
                    if download_link:
                        return Response({'success': 'success', 'downloadURL': download_link}, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'Download link could not be generated.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    # Return error response if an exception occurs
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

            #============= EVI ==========*/
            if action == 'get-evi-map':
                data = core.getEVIMap(refLow, refHigh, studyLow, studyHigh)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'get-evi-pie':
                file_path = 'static/data/evi/pie/'+area_type+"_"+area_id+"_"+refLow+"_"+refHigh+"_"+studyLow+"_"+studyHigh+".json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'rb') as file:
                        data = orjson.loads(file.read())
                        return Response(data)
                else:
                    data = core.calcPie(refLow, refHigh, studyLow, studyHigh)
                    if data:
                        with open(file_path, 'wb') as f:
                            f.write(orjson.dumps(data))
                        return Response(data)
                    else:
                        return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)

            elif action == 'get-evi-line':
                file_path = 'static/data/evi/line/'+area_type+"_"+area_id+"_"+refLow+"_"+refHigh+"_"+studyLow+"_"+studyHigh+".json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'rb') as file:
                        data = orjson.loads(file.read())
                        return Response(data)
                else:
                    data = core.GetPolygonTimeSeries(refLow, refHigh, studyLow, studyHigh)
                    if data:
                        with open(file_path, 'wb') as f:
                            f.write(orjson.dumps(data))
                        return Response(data)
                    else:
                        return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
                
            elif action == 'download-evi-map':
                data = core.getDownloadEVIMap(refLow, refHigh, studyLow, studyHigh)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            #=============== LandCover ===================*/
            elif action == 'get-landcover-map':
                data = core.getLandCoverMap(year)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-landcover-map':
                data = core.getDownloadLandcoverMap(year)
                return Response(data)
                
            elif action == 'get-landcover-chart':
                if area_type == 'country' or area_type == 'province' or area_type == 'district' or area_type == 'protected_area':
                    data = dbcore.get_landcover_stat(studyLow, studyHigh)
                else:
                    data = core.getLandcoverArea(studyLow, studyHigh)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
               
            elif action == 'get-landcover-rice-map':
                data = core.getLandCoverRiceMap(year)
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)

            elif action == 'get-landcover-rubber-map':
                data = core.getLandCoverRubberMap(year)
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)

            elif action == 'download-landcover-rice-map':
                data = core.downloadLandcoverRiceMap(year)
                return Response(data)

            elif action == 'download-landcover-rubber-map':
                data = core.downloadLandcoverRubberMap(year)
                return Response(data)

            elif action == 'get-landcover-rice-line-data':
                if area_type == 'country' or area_type == 'province' or area_type == 'district' or area_type == 'protected_area':
                    data = dbcore.get_landcover_stat(studyLow, studyHigh, landcover_type='rice')
                else:
                    data = core.getLandcoverRiceArea(studyLow, studyHigh)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
                
            elif action == 'get-landcover-rubber-line-data':
                if area_type == 'country' or area_type == 'province' or area_type == 'district' or area_type == 'protected_area':
                    data = dbcore.get_landcover_stat(studyLow, studyHigh, landcover_type='rubber')
                else:
                    data = core.getLandcoverRubberArea(studyLow, studyHigh)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
                
            elif action == 'get-landcover-baselinemeasure-area':
                file_path = f"static/data/lulc/{land_cover_type}_bmarea_{area_type}_{area_id}_{refLow}_{refHigh}_{studyLow}_{studyHigh}.json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'rb') as file:
                        data = orjson.loads(file.read())
                        return Response(data)
                else:
                    data = core.getLCBaselineMeasureArea(refLow, refHigh, studyLow, studyHigh, land_cover_type)
                    if data:
                        # Create directories if they don't exist
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        with open(file_path, 'wb') as f:
                            f.write(orjson.dumps(data))
                        # print(data)
                        return Response(data)
                    else:
                        return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
                
            #============= Forest Monitoring ==========*/
            elif action == 'get-forest-gain-map':
                data = core.getForestGainMap(False, studyLow, studyHigh, tree_canopy_definition, tree_height_definition)
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-forest-gain-map':
                data = core.getForestGainMap(False, studyLow, studyHigh, tree_canopy_definition, tree_height_definition, download='True')
                return Response(data)
                
            elif action == 'get-forest-loss-map':
                data = core.getForestLossMap(False, studyLow, studyHigh, tree_canopy_definition, tree_height_definition)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-forest-loss-map':
                data = core.getForestLossMap(False, studyLow, studyHigh, tree_canopy_definition, tree_height_definition, download='True')
                return Response(data)

            elif action == 'get-forest-extent-map':
                data = core.getForestExtendMap(studyLow, studyHigh, tree_canopy_definition, tree_height_definition, area_type, area_id)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-forest-extent-map':
                data = core.getForestExtendMap(studyLow, studyHigh, tree_canopy_definition, tree_height_definition, area_type, area_id, year=year, download='True')
                return Response(data)

            elif action == 'get-forest-nonforest-chart-data':
                if area_type == 'country' or area_type == 'province' or area_type == 'district' or area_type == 'protected_area':
                    data = dbcore.get_forest_monitoring_stat(studyLow, studyHigh)
                else:
                    data = core.getForestNonForestArea(studyLow, studyHigh, tree_canopy_definition, tree_height_definition, area_type, area_id)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
                
            elif action == 'get-forest-gainloss-area':
                file_path = 'static/data/forest/fgainloss_'+area_type+"_"+area_id+"_"+studyLow+"_"+studyHigh+".json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.getForestGainLossArea(studyLow, studyHigh, tree_canopy_definition, tree_height_definition)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
                        return Response(data)
                    else:
                        return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'get-forest-change-gainloss-chart-data':
                file_path = 'static/data/forest/fcgainloss_'+area_type+"_"+area_id+"_"+studyLow+"_"+studyHigh+".json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.getForestChangeGainLoss(studyLow, studyHigh, refLow, refHigh, tree_canopy_definition, tree_height_definition)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
                        return Response(data)
                    else:
                        return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            #============= Forest Alert ==========*/
            elif action == 'get-glad-alert-map':
                data = core.getGLADAlertMap(year)
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-gladalert-map':
                data = core.downloadGLADAlertMap(year)
                return Response(data)

            elif action == 'get-glad-alert-chart-data':
                if area_type == 'country' or area_type == 'province' or area_type == 'district' or area_type == 'protected_area':
                    data = dbcore.get_glad_alert_stat(studyLow, studyHigh)
                else:
                    data = core.getGLADAlertArea(studyLow, studyHigh, area_type, area_id)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
                
            elif action == 'get-sar-alert-map':
                data = core.getSARAlertMap(year)
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-saralert-map':
                data = core.downloadSARAlertMap(year)
                return Response(data)

            elif action == 'get-sar-alert-chart-data':
                if area_type == 'country' or area_type == 'province' or area_type == 'district' or area_type == 'protected_area':
                    data = dbcore.get_sar_alert_stat(studyLow, studyHigh)
                else:
                    data = core.getSARAlertArea(studyLow, studyHigh, area_type, area_id)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
                
            #============= Fire Hotspot Monitoring ==========*/
            elif action == 'get-burned-area':
                data = core.getBurnedMap(year, area_type)
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-burned-area-map':
                data = core.downloadFirmBurnedArea(year)
                return Response(data)

            elif action == 'get-burned-area-chart-data':
                if area_type == 'country' or area_type == 'province' or area_type == 'district' or area_type == 'protected_area':
                    data = dbcore.get_fire_hotspot_stat(studyLow, studyHigh)
                else:
                    data = core.getBurnedArea(studyLow, studyHigh, area_type, area_id)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
                
            #=============== Drought Monitoring ========================>
            elif action == 'get-drought-index-dates':
                data = core.get_date_from_drought_index_collection(index)
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'get-drought-index-map':
                data = core.getDroughtIndexMap(index, date)
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-drought-index-map':
                data = core.downloadDroughtIndexMap(index, date)
                return Response(data)
            
            # Short-term weather
            elif action == 'get-weather-map':
                data = core.get_weather_map(weather_param, weather_type, download="False")
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-weather-map':
                data = core.get_weather_map(weather_param, weather_type, download="True")
                return Response(data)
            
            #=============== Forest Changes  ========================>
            elif action == 'get-forestchange-chart':
                if area_type == 'country' or area_type == 'province' or area_type == 'district' or area_type == 'protected_area':
                    data = dbcore.get_forestchanges_stat(studyLow, studyHigh)
                else:
                    data = core.getLandcoverArea(studyLow, studyHigh)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
        
            #=============== Combined Deforestation Alert ========================>
            elif action == 'get-glad-deforestation-alert-map':
                data = core.get_deforestation_alert_map(start_date, end_date, "glad", download="False")

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'get-combined-deforestation-alert-map':
                data = core.get_deforestation_alert_map(start_date, end_date, "combinedAlerts", download="False")

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'get-doy-glad-deforestation-alert-map':
                data = core.get_doy_glad_deforestation_alert_map(year=year, doy=doy, download="False")

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-glad-deforestation-alert-map':
                data = core.get_deforestation_alert_map(start_date, end_date, "glad", download="True")

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-combined-deforestation-alert-map':
                data = core.get_deforestation_alert_map(start_date, end_date, "combinedAlerts", download="True")

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'download-doy-glad-deforestation-alert-map':
                data = core.get_doy_glad_deforestation_alert_map(year=year, doy=doy, download="True")

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'get-sar-biweekly-alert':
                data = core.get_sar_biweekly_alert_map(year=year, download="False")

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)

            elif action == 'download-sar-biweekly-alert':
                data = core.get_sar_biweekly_alert_map(year=year, download="True")

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
                 

    return Response({'error': 'Bad request, action parameter is required or not valid.'}, status=status.HTTP_400_BAD_REQUEST)