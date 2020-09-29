from django.contrib.gis.db import models


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