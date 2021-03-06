import requests
from django.contrib.gis.geos import Point as P
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from datum_gis.models import (Point, Line)
from datum_gis.serializers import (ViewLineSerializer, ViewPointSerializer,
                                   LoadDataSerialaser, PointSerachSerialaizer,
                                   ShowResultsScoreSerialaizer, ShowResultsDistanceSerialaizer)
from datum_gis.utils import (short_path, short_score, short_distance, short_path_score)


class PointView(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ViewPointSerializer
    queryset = Point.objects.all()


class LineView(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ViewLineSerializer
    queryset = Line.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
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

        return Response(data={'points': created_p, 'lines': created_l}, status=status.HTTP_200_OK)


class MinLenght(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShowResultsDistanceSerialaizer

    def get_min_lenght(self, request, *args, **kwargs):
        serializer = PointSerachSerialaizer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        short_distanse_list = short_distance(serializer.data['start'])
        show_path = short_path(serializer.data['start'], serializer.data['end'], short_distanse_list)
        serializer = self.get_serializer(show_path)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class MinScore(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShowResultsScoreSerialaizer

    def get_min_score(self, request, *args, **kwargs):
        serializer = PointSerachSerialaizer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        short_distanse_list = short_score(serializer.data['start'])
        show_path = short_path_score(serializer.data['start'], serializer.data['end'], short_distanse_list)
        serializer = self.get_serializer(show_path)
        return Response(data=serializer.data, status=status.HTTP_200_OK)