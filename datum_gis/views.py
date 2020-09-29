import requests
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from datum_gis.models import (Point, Line)
from datum_gis.serializers import (ViewLineSerializer, ViewPointSerializer,
                                   LoadDataSerialaser)
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.response import Response


class PointView(ModelViewSet):
    serializer_class = ViewPointSerializer
    queryset = Point.objects.all()


class LineView(ModelViewSet):
    serializer_class = ViewLineSerializer
    queryset = Line.objects.all()


class LoadData(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoadDataSerialaser

    def get_public_api(self, request):
        url = 'https://datum-test-task.firebaseio.com/api/lines-points.json'
        response = requests.get(url)
        print(response.content)

        serializer = LoadDataSerialaser(data=response.content)
        if serializer.is_valid(raise_exception=True):
            gis = serializer.save()
            gis_serializer = self.get_serializer(gis)
        return Response(data=gis_serializer.data, status=status.HTTP_201_CREATED)
