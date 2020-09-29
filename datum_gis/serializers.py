from rest_framework import serializers
from datum_gis.models import (Point, Line)


class ViewPointSerializer(serializers.Serializer):

    class Meta:
        models = Point
        fields = '__all__'


class ViewLineSerializer(serializers.Serializer):

    class Meta:
        models = Line
        fields = '__all__'


class LoadDataSerialaser(serializers.Serializer):
    point = ViewPointSerializer()
    line = ViewLineSerializer()