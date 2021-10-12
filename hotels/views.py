from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.views.generic import (
    DetailView, ListView, CreateView, UpdateView, DeleteView)
import datetime

from django.shortcuts import get_object_or_404, redirect
from django.http import (
    HttpResponseRedirect,
)
from hotels.forms import (
    ReviewCreationForm,
    HotelFilterForm,
    HotelCreationForm, HotelUpdateForm,
    CityCreationForm, CityUpdateForm, CityDeleteForm, RoomUpdateForm,
    RoomCreationForm, BookingCreationForm,
)

from hotels.models import Hotel, Room, Review, Booking, City
from django.contrib import messages
from django.urls import reverse_lazy
import json
from utils.mixins import AjaxFormMixin, MyPermissionRequiredMixin


class RoomCreateView(MyPermissionRequiredMixin, AjaxFormMixin, CreateView):
    permission_required = 'hotels.add_room'
    permission_denied_message = 'Недостаточно прав'

    model = Room
    form_class = RoomCreationForm
    template_name = 'hotels/room_create.html'

    def get_success_url(self):
        messages.success(self.request, 'Номер создан успешно')
        # #Согласно документации, get_success_url
        # должен просто возвращать URL для перенаправления, а не ответ на перенаправление
        str_url = self.request.environ['HTTP_REFERER']
        return str_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' добавление номеров'
        context['hotel_id'] = self.kwargs['hotel_id']
        context['hotel'] = Hotel.objects.get(pk=self.kwargs['hotel_id'])
        context['create_room'] = RoomCreationForm(self.request.POST)
        return context


def room_unbooking(request, pk):
    # вызывается из booking_list.html
    book = get_object_or_404(Booking, pk=pk)
    # удалить запись из Booking
    book.delete()
    messages.success(request,
                     f'Бронь этого номера успешно снята')

    return redirect('accounts:booking_list')


class RoomUpdateView(MyPermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'hotels.change_room'
    permission_denied_message = 'Недостаточно прав'

    template_name = 'hotels/room_update.html'
    model = Room
    form_class = RoomUpdateForm
    success_message = 'Номер успешно изменен.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' редактирование номера'
        return context

    def get_success_url(self):
        # Согласно документации, get_success_url
        # должен просто возвращать URL для перенаправления, а не ответ на перенаправление
        return self.object.get_absolute_url()

    def form_valid(self, form):
        room = self.object
        if not room.is_booking:
            book_id = room.get_booking_last
            if book_id:  # если есть соответствие в Booking:
                book = Booking.objects.get(pk=book_id)
                date_end = book.date_end
                today = datetime.date.today()
                if today <= date_end:
                    # удалить запись из Booking
                    book.delete()
                    messages.success(self.request,
                                     f'Бронь этого номера успешно снята')
        else:
            messages.success(self.request, f'Номер успешно забронирован')
        return super().form_valid(form)


class CityDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'hotels/city_delete.html'
    model = City
    form_class = CityDeleteForm
    success_message = 'Город успешно удален.'
    success_url = reverse_lazy('accounts:dashboard')


class CityUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'hotels/city_update.html'
    model = City
    form_class = CityUpdateForm
    success_message = 'Город успешно изменен.'

    def get_success_url(self):
        # Согласно документации, get_success_url
        # должен просто возвращать URL для перенаправления, а не ответ на перенаправление
        str_url = self.request.environ['HTTP_REFERER']
        return str_url


class CityCreateView(SuccessMessageMixin, CreateView):
    template_name = 'hotels/city_create.html'
    form_class = CityCreationForm
    success_message = 'Город успешно добавлен.'

    def get_success_url(self):
        # Согласно документации, get_success_url
        # должен просто возвращать URL для перенаправления, а не ответ на перенаправление
        str_url = self.request.environ['HTTP_REFERER']
        return str_url

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        nexturl = self.request.META.get('HTTP_REFERER', None) or '/'
        # reverse_lazy - не работает!!!!
        return HttpResponseRedirect(nexturl)


class ReviewCreationView(MyPermissionRequiredMixin, CreateView):
    permission_required = 'hotels.add_review'
    permission_denied_message = 'Недостаточно прав'

    model = Review
    form_class = ReviewCreationForm

    def get_success_url(self):
        return self.object.hotel.get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request,
                         f'Отзыв добавлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return HttpResponseRedirect(form.get_redirect_url())


class HotelCreateView(MyPermissionRequiredMixin, CreateView):
    permission_required = 'hotels.add_hotel'
    permission_denied_message = 'Недостаточно прав'

    model = Hotel
    template_name = 'hotels/hotel_update.html'
    form_class = HotelCreationForm

    # переход в случае успеха. По умолчанию, если не указать -
    # переход на детальную страницу
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Отель создан успешно')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' добавление отеля'
        return context


class HotelUpdateView(MyPermissionRequiredMixin, CityUpdateView, UpdateView):
    permission_required = 'hotels.change_hotel'
    permission_denied_message = 'Недостаточно прав'

    model = Hotel
    template_name = 'hotels/hotel_update.html'
    form_class = HotelUpdateForm

    def get_context_data(self, **kwargs):
        hotel = self.object
        context = super().get_context_data(**kwargs)
        context['title'] = ' редактирование отеля'
        initial = {
            'cityname': City.objects.get(pk=hotel.city_id).get_city,
            'country': hotel.country_id,
            'pk': hotel.city_id,
            'hotel_id': hotel.id
        }
        context['id_city'] = hotel.city_id
        context['city'] = CityCreationForm
        context['update_city'] = CityUpdateForm(initial=initial)
        context['delete_city'] = CityDeleteForm(initial={
            'cityname': City.objects.get(pk=hotel.city_id),
            'pk': hotel.city_id
        })
        return context

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = super().get_queryset().filter(pk=pk)
        queryset = queryset.EvQuSet()
        return queryset


class HotelDetailView(MyPermissionRequiredMixin, DetailView):
    permission_required = 'hotels.view_hotel'
    permission_denied_message = 'Недостаточно прав'

    model = Hotel
    template_name = 'hotels/hotel_booking.html'  # по умолчанию: 'hotel_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_date_start = False
        filter_date_end = False

        if 'filter' in self.request.session:
            filter_dist = self.request.session['filter']
            if filter_dist.__contains__('date_start'):
                try:
                    filter_date_start = datetime.datetime.strptime(filter_dist['date_start'], "%Y-%m-%d").date()
                except:
                    filter_date_start = False

            if filter_dist.__contains__('date_end'):
                try:
                    filter_date_end = datetime.datetime.strptime(filter_dist['date_end'], "%Y-%m-%d").date()
                except:
                    filter_date_end = False

        if not filter_date_start:
            indate = self.request.GET.get("d_start")
            if indate:
                filter_date_start = datetime.datetime.strptime(indate, "%Y-%m-%d").date()

        if not filter_date_end:
            indate = self.request.GET.get("d_end")
            if indate:
                filter_date_end = datetime.datetime.strptime(indate, "%Y-%m-%d").date()

        obrooms = list(context['hotel'].rooms.all())

        # проверять на дату начала есть ли свободные места!!!!!!!!!!!!!!!!!!!!
        available = False
        rooms = []
        for room in obrooms:
            room.is_booking = True
            if room.bookings.values():
                obbookings = list(room.bookings.values())
                for book in obbookings:
                    dts = book['date_start']
                    dte = book['date_end']
                    if filter_date_start and dts and dte:
                        if filter_date_start > dte:
                            available = True
                            room.is_booking = False
                            break
                        elif filter_date_end < dts:
                            available = True
                            room.is_booking = False
                            break
                    else:
                        available = True
                        room.is_booking = False
            else:
                available = True
                room.is_booking = False

            rooms.append(room)

        category = list('*' * int(self.object.category))
        review_form = ReviewCreationForm(
            initial={
                'user': self.request.user,
                'user_pk': self.request.user.pk,
                'hotel': self.object,
                'created': datetime.date.today().strftime('%Y-%m-%d')
            }
        )

        context = {
            'user': self.request.user,
            'hotel': self.object,
            'category': category,
            'filter_date_start': filter_date_start,
            'filter_date_end': filter_date_end,
            'available': available,
            'rooms': rooms,
            'review_form': review_form
        }
        return context

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk == 0:
            pk = self.request.GET.get("pk")
            self.kwargs['pk'] = pk

        queryset = super().get_queryset().filter(pk=pk)
        queryset = queryset.EvQuSet()
        return queryset


class HotelListView(ListView):
    model = Hotel
    template_name = 'hotels/hotels_list.html'  # необязательно, указать, если имя шаблона отличается от стандартного
    context_object_name = 'hotels_objects'  # по умолчанию: = object_list
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = HotelFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.EvQuSet()
        # начало обработки запроса GET для запоминариня фильтров
        filter_dist = {}
        # если был переход по страниицам
        page = self.request.GET.get('page', None)

        if 'filter' in self.request.session:
            filter_dist = self.request.session['filter']

            if page:
                # добавить 'page' к session['filter']
                filter_dist.update({'page': page})
            else:
                if self.request.GET:
                    # поностью обновить session['filter']
                    del self.request.session['filter']
                    filter_dist = self.request.GET.copy()

            if len(filter_dist) > 0:
                self.request.session['filter'] = filter_dist
                self.request.GET = filter_dist
        else:
            filter_dist = self.request.GET.copy()
        # конец обработки запроса GET для запоминариня фильтров

        # обработка фильтров
        if filter_dist.__contains__('country'):
            filter_country = self.request.GET.get('country', '')
            filter_dist['country'] = filter_country
        else:
            filter_country = None

        if filter_dist.__contains__('date_start'):
            filter_date_start = self.request.GET.get('date_start', '')
            filter_dist['date_start'] = filter_date_start
        else:
            filter_date_start = None

        if filter_dist.__contains__('date_end'):
            filter_date_end = self.request.GET.get('date_end', '')
            filter_dist['date_end'] = filter_date_end
        else:
            filter_date_end = None

        if filter_dist.__contains__('is_available'):
            filter_is_available = self.request.GET.get('is_available', '')
            filter_dist['is_available'] = filter_is_available
        else:
            filter_is_available = None

        if filter_dist.__contains__('min_price'):
            filter_min_price = self.request.GET.get('min_price', '')
            filter_dist['min_price'] = filter_min_price
        else:
            filter_min_price = None

        if filter_dist.__contains__('max_price'):
            filter_max_price = self.request.GET.get('max_price', '')
            filter_dist['max_price'] = filter_max_price
        else:
            filter_max_price = None

        if filter_dist.__contains__('category'):
            q = json.loads(json.dumps(dict(filter_dist)))
            filter_category = q['category']
            filter_dist['category'] = filter_category
        else:
            filter_category = None

        if filter_dist.__contains__('service'):
            q = json.loads(json.dumps(dict(filter_dist)))
            filter_service = q['service']
            filter_dist['service'] = filter_service
        else:
            filter_service = None

        if page:
            filter_dist['page'] = page

        if len(filter_dist) > 0:
            self.request.session['filter'] = filter_dist

        if filter_country:
            queryset = queryset.filter(country=filter_country)

        if filter_date_start:
            if filter_date_end:
                queryset = queryset.exclude(Q(rooms__bookings__date_start__gte=filter_date_start) &
                                            Q(rooms__bookings__date_end__lte=filter_date_end))
            else:
                queryset = queryset.exclude(Q(rooms__bookings__date_start__gte=filter_date_start))

        if filter_is_available:
            queryset = queryset.filter(rooms__is_booking=False)
        if filter_category:
            # условие ИЛИ
            queryset = queryset.filter(category__in=filter_category)
        if filter_min_price:
            queryset = queryset.filter(rooms__price__gte=filter_min_price)
        if filter_max_price:
            queryset = queryset.filter(rooms__price__lte=filter_max_price)
        if filter_service:
            # условие И
            for service in filter_service:
                ls = []
                # по устовию МНОГО надо каждый переводить в list!!!!!
                ls.append(service)
                queryset = queryset.filter(service__in=ls)

        queryset = queryset.order_by('-pk')
        return queryset


class RoomBookingView(MyPermissionRequiredMixin, CreateView):
    permission_required = 'hotels.add_booking'
    permission_denied_message = 'Недостаточно прав'

    model = Booking
    form_class = BookingCreationForm
    success_url = reverse_lazy('accounts:booking_list')  # переход в случае успеха.

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        room = form.cleaned_data.get('room', None)

        user = form.cleaned_data.get('user', None)
        if user is None:
            messages.error(self.request,
                           f'Юзер не задан')
        if room is None:
            room_id = self.kwargs['room_id']
            room = get_object_or_404(Room, pk=room_id)

        redirect_url = room.get_absolute_url() if room else reverse_lazy('hotels:hotel_detail')
        return HttpResponseRedirect(redirect_url)

    def form_valid(self, form):
        room_id = self.request.POST['room']
        theroom = Room.objects.get(pk=room_id)
        theroom.is_booking = True
        theroom.save()

        messages.success(self.request,
                         f'Ваше бронирование успешно завершено')
        return super().form_valid(form)
