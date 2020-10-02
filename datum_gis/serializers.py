from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from django.contrib.gis.geos import Point as point
from datum_gis.models import (Point, Line)


class ViewPointSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Point
        geo_field = 'geom'
        fields = ['score', 'geom']


class ViewLineSerializer(serializers.Serializer):
    from_point = serializers.SerializerMethodField()
    to_point = serializers.SerializerMethodField()

    class Meta:
        model = Line
        fields = ['from_point', 'to_point']

    def get_from_point(self, obj):
        return obj.from_point.pk

    def get_to_point(self, obj):
        return obj.to_point.pk

class LoadDataSerialaser(serializers.Serializer):
    points = ViewPointSerializer(many=True)
    lines = ViewLineSerializer(many=True)


class PointSerachSerialaizer(serializers.Serializer):
    start = serializers.IntegerField()
    end = serializers.IntegerField()
