from geojson_serializer.serializers import geojson_serializer
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

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


@geojson_serializer('point')
class PointSerialaizer(serializers.Serializer):
    point = serializers.SerializerMethodField()

    def get_point(self, obj):
        geom = Point.objects.get(pk=obj).geom
        return geom


class ShowResultsDistanceSerialaizer(serializers.Serializer):
    distance = serializers.SerializerMethodField()
    points = PointSerialaizer(many=True)

    def get_distance(self, obj):
        return obj['distance']


class ShowResultsScoreSerialaizer(serializers.Serializer):
    score = serializers.SerializerMethodField()
    points = PointSerialaizer(many=True)

    def get_score(self, obj):
        return obj['score']

