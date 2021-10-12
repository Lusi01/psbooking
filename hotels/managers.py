from django.db import models
from django.db.models import Count
from django.db.models.functions import Coalesce


class EventQuerySet(models.QuerySet):

    def with_counts(self):
        return self.annotate(
            count_rooms=Coalesce(models.Count('rooms'), 0),
            sum_rate=Coalesce(models.Sum('reviews__rate'), 0),
            c_rate=Coalesce(models.Count('reviews'), 1),
            count_reviews=Count('reviews__rate'),
            new_rate=models.F('sum_rate') * 10 / models.F('c_rate') * 0.1,
        )

    def EvQuSet(self):
        return self.select_related('city').prefetch_related(
            'rooms__bookings__user',
            'service',
            'reviews__user').with_counts()
