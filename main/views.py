from django.db.models import Min, Prefetch, F
from django.views.generic import TemplateView

from hotels.models import Country, Hotel, Review
from main.forms import (
    MainFilterForm,
)


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filter_form'] = MainFilterForm(self.request.GET)
        context['review_list'] = Review.objects.select_related('hotel').all().order_by('-updated')[:3]

        hotel_list = Hotel.objects.prefetch_related('reviews', 'rooms').with_counts().all().order_by(
            '-count_reviews')[:3]
        context['hotel_list'] = hotel_list

        dl = Prefetch('hotels', queryset=Hotel.objects.all(), to_attr='all_hotels_list')
        destination_list = Country.objects.prefetch_related(dl).annotate(
            new_price=Min('hotels__rooms__price') / 1000.0,
            hotel_logo=F('hotels__logo'),
        ).all().order_by('-pk')[:3]
        context['destination_list'] = destination_list
        context['special_content'] = True

        context['d_start'] = ''
        context['d_end'] = ''
        context['pk'] = 0

        return context
