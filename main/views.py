import os, json
from django.shortcuts import render
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .core import GEEApi

@csrf_exempt 
@api_view(['GET'])
@permission_classes([AllowAny])
def api(request):
    get = request.query_params.get
    action = get('action', '')

    if action:
        request_methods = [
            'get-landcover-rice-map', 
            'get-landcover-rubber-map',
            'get-landcover-rice-line-data',
            'get-landcover-rubber-line-data',
            'download-landcover-rice-map',
            'download-landcover-rubber-map'
        ]

        if action in request_methods:
            area_type = get('area_type', '')
            area_id = get('area_id', '')
            refLow = get('refLow', '')
            refHigh = get('refHigh', '')
            studyLow = get('studyLow', '')
            studyHigh = get('studyHigh', '')
            year = get('year', '')

            core = GEEApi(area_type, area_id)

            if action == 'get-landcover-rice-map':
                data = core.getLandCoverRiceMap(year)
            elif action == 'get-landcover-rubber-map':
                data = core.getLandCoverRubberMap(year)
            elif action == 'download-landcover-rice-map':
                data = core.downloadLandcoverRiceMap(year)
            elif action == 'download-landcover-rubber-map':
                data = core.downloadLandcoverRubberMap(year)
            elif action == 'get-landcover-rice-line-data':
                data = core.getLandcoverRiceArea(studyLow, studyHigh)
            elif action == 'get-landcover-rubber-line-data':
                data = core.getLandcoverRubberArea(studyLow, studyHigh)
            
    return Response(data)

@csrf_exempt 
@api_view(['GET'])
def get_evi_map(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    core = GEEApi(area_type, area_id)
    refLow = request.GET.get('refLow')
    refHigh = request.GET.get('refHigh')
    studyLow = request.GET.get('studyLow')
    studyHigh = request.GET.get('studyHigh')
    data = core.getEVIMap(refLow, refHigh, studyLow, studyHigh)
    # print(data)
    return Response(data)

@csrf_exempt 
@api_view(['GET'])
def get_pie_evi(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    refLow = request.GET.get('refLow')
    refHigh = request.GET.get('refHigh')
    studyLow = request.GET.get('studyLow')
    studyHigh = request.GET.get('studyHigh')
    file_path = 'static/data/evi/pie/'+area_type+"_"+area_id+"_"+refLow+"_"+refHigh+"_"+studyLow+"_"+studyHigh+".json"
    if os.path.exists(file_path):
        # Read and parse the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        core = GEEApi(area_type, area_id)
        data = core.calcPie(refLow, refHigh, studyLow, studyHigh)
        with open(file_path, 'w') as f:
            json.dump(data, f)
    return Response(data)

@csrf_exempt 
@api_view(['GET'])
def get_line_evi(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    refLow = request.GET.get('refLow')
    refHigh = request.GET.get('refHigh')
    studyLow = request.GET.get('studyLow')
    studyHigh = request.GET.get('studyHigh')
    file_path = 'static/data/evi/line/'+area_type+"_"+area_id+"_"+refLow+"_"+refHigh+"_"+studyLow+"_"+studyHigh+".json"
    if os.path.exists(file_path):
        # Read and parse the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        core = GEEApi(area_type, area_id)
        data = core.GetPolygonTimeSeries(refLow, refHigh, studyLow, studyHigh)
        with open(file_path, 'w') as f:
            json.dump(data, f)
    return Response(data)

@csrf_exempt 
@api_view(['GET'])
def get_download_evi_map(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    core = GEEApi(area_type, area_id)
    refLow = request.GET.get('refLow')
    refHigh = request.GET.get('refHigh')
    studyLow = request.GET.get('studyLow')
    studyHigh = request.GET.get('studyHigh')
    data = core.getDownloadEVIMap(refLow, refHigh, studyLow, studyHigh)
    return Response(data)

#=================== Landcover =============================>
@csrf_exempt 
@api_view(['GET'])
def get_landcover_map(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    core = GEEApi(area_type, area_id)
    year = request.GET.get('year')
    data = core.getLandCoverMap(year)
    # print(data)
    return Response(data)

@csrf_exempt 
@api_view(['GET'])
def get_download_landcover_map(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    core = GEEApi(area_type, area_id)
    year = request.GET.get('year')
    data = core.getDownloadLandcoverMap(year)
    return Response(data)

@csrf_exempt 
@api_view(['GET'])
def get_landcover_stats(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    start_year = request.GET.get('studyLow')
    end_year = request.GET.get('studyHigh')
    file_path = 'static/data/lulc/'+area_type+"_"+area_id+"_"+start_year+"_"+end_year+".json"
    if os.path.exists(file_path):
        # Read and parse the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        core = GEEApi(area_type, area_id)
        data = core.getLandcoverArea(start_year, end_year)
        with open(file_path, 'w') as f:
            json.dump(data, f)
    # core = GEEApi(area_type, area_id)
    # data = core.getLandcoverArea(start_year, end_year)
    # print(data)
    return Response(data)

#=================== Landcover Rice =============================>
@csrf_exempt 
@api_view(['GET'])
def get_landcover_rice_map(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    core = GEEApi(area_type, area_id)
    year = request.GET.get('year')
    data = core.getLandCoverRiceMap(year)
    # print(data)
    return Response(data)

@csrf_exempt 
@api_view(['GET'])
def get_download_landcover_rice_map(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    core = GEEApi(area_type, area_id)
    year = request.GET.get('year')
    data = core.getDownloadLandcoverRiceMap(year)
    return Response(data)

@csrf_exempt 
@api_view(['GET'])
def get_landcover_rice_stats(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    start_year = request.GET.get('studyLow')
    end_year = request.GET.get('studyHigh')
    file_path = 'static/data/lulc/rice/lc_rice_'+area_type+"_"+area_id+"_"+start_year+"_"+end_year+".json"
    if os.path.exists(file_path):
        # Read and parse the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        core = GEEApi(area_type, area_id)
        data = core.getLandcoverRiceArea(start_year, end_year)
        with open(file_path, 'w') as f:
            json.dump(data, f)
    # core = GEEApi(area_type, area_id)
    # data = core.getLandcoverRiceArea(start_year, end_year)
    # print(data)
    return Response(data)

#=================== Landcover Rubber =============================>
@csrf_exempt 
@api_view(['GET'])
def get_landcover_rubber_map(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    core = GEEApi(area_type, area_id)
    year = request.GET.get('year')
    data = core.getLandCoverRubberMap(year)
    # print(data)
    return Response(data)

@csrf_exempt 
@api_view(['GET'])
def get_download_landcover_rubber_map(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    core = GEEApi(area_type, area_id)
    year = request.GET.get('year')
    data = core.getDownloadLandcoverRubberMap(year)
    return Response(data)

@csrf_exempt 
@api_view(['GET'])
def get_landcover_rubber_stats(request):
    area_id = request.GET.get('area_id')
    area_type = request.GET.get('area_type')
    # print(area_id, area_type)
    start_year = request.GET.get('studyLow')
    end_year = request.GET.get('studyHigh')
    file_path = 'static/data/lulc/rubber/lc_rubber_'+area_type+"_"+area_id+"_"+start_year+"_"+end_year+".json"
    if os.path.exists(file_path):
        # Read and parse the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        core = GEEApi(area_type, area_id)
        data = core.getLandcoverRubberArea(start_year, end_year)
        with open(file_path, 'w') as f:
            json.dump(data, f)
    # core = GEEApi(area_type, area_id)
    # data = core.getLandcoverRubberArea(start_year, end_year)
    # print(data)
    return Response(data)