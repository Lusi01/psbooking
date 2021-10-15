from django.db import models
from django.db.models import Count, Max
from django.db.models.functions import Coalesce


class EventQuerySet(models.QuerySet):

    def with_counts(self):
        return self.annotate(
            count_reviews=Count('reviews__rate'),
        )

    def EvQuSet(self):
        return self.select_related('city').prefetch_related(
            'rooms__bookings__user',
            'service',
            'reviews__user').with_counts()
