from django.db import models


class City(models.Model):

    name = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()

    class Meta:
        verbose_name_plural = 'cities'
        indexes = [
            models.Index(fields=['name'], name='city_name_idx'),
        ]
