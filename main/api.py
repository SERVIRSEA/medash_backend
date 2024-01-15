import os, json
from django.shortcuts import render
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .core import GEEApi
from .authentication import APIKeyAuthentication

@csrf_exempt 
@api_view(['GET'])
@authentication_classes([APIKeyAuthentication])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def api(request):
    action = request.query_params.get('action', '')

    if action:
        request_methods = [
            'get-evi-map',
            'get-evi-pie',
            'get-evi-line',
            'download-evi-map',
            'get-landcover-map',
            'get-landcover-chart',
            'get-landcover-rice-map', 
            'get-landcover-rubber-map',
            'get-landcover-rice-line-data',
            'get-landcover-rubber-line-data',
            'download-landcover-rice-map',
            'download-landcover-rubber-map',
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
            'get-landcover-baselinemeasure-area',
        ]

        if action in request_methods:
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

            core = GEEApi(area_type, area_id)

            tree_canopy_definition = 10
            tree_height_definition = 5 

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
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.calcPie(refLow, refHigh, studyLow, studyHigh)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
                        return Response(data)
                    else:
                        return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'get-evi-line':
                file_path = 'static/data/evi/line/'+area_type+"_"+area_id+"_"+refLow+"_"+refHigh+"_"+studyLow+"_"+studyHigh+".json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.GetPolygonTimeSeries(refLow, refHigh, studyLow, studyHigh)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
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
            
            elif action == 'get-landcover-chart':
                file_path = 'static/data/lulc/'+area_type+"_"+area_id+"_"+studyLow+"_"+studyHigh+".json"
                
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.getLandcoverArea(studyLow, studyHigh)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
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
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)

            elif action == 'download-landcover-rubber-map':
                data = core.downloadLandcoverRubberMap(year)
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)

            elif action == 'get-landcover-rice-line-data':
                file_path = 'static/data/lulc/rice/lc_rice_'+area_type+"_"+area_id+"_"+studyLow+"_"+studyHigh+".json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.getLandcoverRiceArea(studyLow, studyHigh)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
                        return Response(data)
                    else:
                        return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)

            elif action == 'get-landcover-rubber-line-data':
                file_path = 'static/data/lulc/rubber/lc_rubber_'+area_type+"_"+area_id+"_"+studyLow+"_"+studyHigh+".json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.getLandcoverRubberArea(studyLow, studyHigh)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
                        return Response(data)
                    else:
                        return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'get-landcover-baselinemeasure-area':
                file_path = f"static/data/lulc/{land_cover_type}_bmarea_{area_type}_{area_id}_{refLow}_{refHigh}_{studyLow}_{studyHigh}.json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.getLCBaselineMeasureArea(refLow, refHigh, studyLow, studyHigh, land_cover_type)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
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
            
            elif action == 'get-forest-loss-map':
                data = core.getForestLossMap(False, studyLow, studyHigh, tree_canopy_definition, tree_height_definition)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'get-forest-extent-map':
                data = core.getForestExtendMap(studyLow, studyHigh, tree_canopy_definition, tree_height_definition, area_type, area_id)

                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'get-forest-nonforest-chart-data':
                file_path = 'static/data/forest/fnf_'+area_type+"_"+area_id+"_"+studyLow+"_"+studyHigh+".json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.getForestNonForestArea(studyLow, studyHigh, tree_canopy_definition, tree_height_definition, area_type, area_id)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
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
            
            elif action == 'get-glad-alert-chart-data':
                file_path = 'static/data/forestalert/glad/glad_'+area_type+"_"+area_id+"_"+studyLow+"_"+studyHigh+".json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.getGLADAlertArea(studyLow, studyHigh, area_type, area_id)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
                        return Response(data)
                    else:
                        return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif action == 'get-sar-alert-map':
                data = core.getSARAlertMap(year)
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)

            elif action == 'get-sar-alert-chart-data':
                file_path = 'static/data/forestalert/sar/sar_'+area_type+"_"+area_id+"_"+studyLow+"_"+studyHigh+".json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.getSARAlertArea(studyLow, studyHigh)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
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
            
            elif action == 'get-burned-area-chart-data':
                file_path = 'static/data/firehotspot/fhs_'+area_type+"_"+area_id+"_"+studyLow+"_"+studyHigh+".json"
                if os.path.exists(file_path):
                    # Read and parse the JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        return Response(data)
                else:
                    data = core.getBurnedArea(studyLow, studyHigh, area_type, area_id)
                    if data:
                        with open(file_path, 'w') as f:
                            json.dump(data, f)
                        return Response(data)
                    else:
                        return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)

            #=============== Drought Monitoring ========================>
            elif action == 'get-drought-index-map':
                data = core.getDroughtIndexMap(index, date)
                if data:
                    return Response(data)
                else:
                    return Response({'error': 'No data found for your request.'}, status=status.HTTP_404_NOT_FOUND)
            
    return Response({'error': 'Bad request, action parameter is required or not valid.'}, status=status.HTTP_400_BAD_REQUEST)