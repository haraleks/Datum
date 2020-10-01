from django.contrib.gis.db import models
from geopy.distance import distance


class Point(models.Model):
    geom = models.PointField()
    score = models.IntegerField(null=True)


class Line(models.Model):
    from_point = models.ForeignKey(
        'datum_gis.Point',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='from_point'
    )
    to_point = models.ForeignKey(
        'datum_gis.Point',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='to_point'
    )

    @property
    def distance_line(self):
        return distance(self.from_point.geom, self.to_point.geom).km
