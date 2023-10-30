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
            'download-landcover-rubber-map'
        ]

        if action in request_methods:
            area_type = request.query_params.get('area_type', '')
            area_id = request.query_params.get('area_id', '')
            refLow = request.query_params.get('refLow', '')
            refHigh = request.query_params.get('refHigh', '')
            studyLow = request.query_params.get('studyLow', '')
            studyHigh = request.query_params.get('studyHigh', '')
            year = request.query_params.get('year', '') 

            core = GEEApi(area_type, area_id)

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
                    
    return Response({'error': 'Bad request, action parameter is required or not valid.'}, status=status.HTTP_400_BAD_REQUEST)