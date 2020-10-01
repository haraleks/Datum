import requests
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from datum_gis.models import (Point, Line)
from datum_gis.serializers import (ViewLineSerializer, ViewPointSerializer,
                                   LoadDataSerialaser)
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point as P


class PointView(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ViewPointSerializer
    queryset = Point.objects.all()


class LineView(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ViewLineSerializer
    queryset = Line.objects.all()

    def list(self, request, *args, **kwargs):
        print(self.queryset)
        serializer = self.get_serializer(self.queryset, context={'request': request}, many=True)
        print(serializer.data)
        return Response(serializer.data)


class LoadData(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoadDataSerialaser

    def get_public_api(self, request):
        url = 'https://datum-test-task.firebaseio.com/api/lines-points.json'
        response = requests.get(url)
        res_json = response.json()
        points = res_json['points']
        lines = res_json['lines']
        for point in points:
            p, created_p = Point.objects.get_or_create(pk=point['obj_id'],
                                                       geom=P(point['lat'], point['lon']),
                                                       score=point['score'])
        for line in lines:
            l, created_l = Line.objects.get_or_create(from_point=Point.objects.get(pk=line['from_obj']),
                                                      to_point=Point.objects.get(pk=line['to_obj']))

        return Response(data={'points': created_p, 'lines': created_l}, status=status.HTTP_201_CREATED)


# class SearchMinScore(ModelViewSet):
#
#     def get_min(self, request):

