from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from hotels.managers import EventQuerySet


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


class Country(models.Model):
    countryname = models.CharField(max_length=250, auto_created=True, default='',
                                   verbose_name='Страна')
    logo = models.ImageField(upload_to='destination/list', blank=True, null=True, verbose_name='Загрузить изображение')

    @property
    def logo_url(self):
        return self.logo.url if self.logo else f'{settings.STATIC_URL}images/destination/destination3.jpg'

    class Meta:
        verbose_name_plural = 'Страны'
        verbose_name = 'Страна'

    def __str__(self):
        return self.countryname


class City(models.Model):
    cityname = models.CharField(unique=True, max_length=250, auto_created=True, verbose_name='Город')
    country = models.ForeignKey(Country, auto_created=True, null=True, verbose_name='Страна',
                                on_delete=models.CASCADE, related_name='cityes')

    def __str__(self):
        return f'{self.cityname}, {self.country}'

    def get_absolute_url(self):
        return reverse('hotels:city_update', args=[str(self.pk)])

    @property
    def get_city(self):
        return f'{self.cityname}'

    class Meta:
        verbose_name_plural = 'Города'
        verbose_name = 'Город'


class Service(models.Model):
    title = models.CharField(max_length=250, default='', verbose_name='Название')

    class Meta:
        verbose_name_plural = 'Сервисы'
        verbose_name = 'Сервис'

    def __str__(self):
        return self.title


class Hotel(models.Model):
    title = models.CharField(max_length=250, default='', verbose_name='Название')
    country = models.ForeignKey(Country, auto_created=True, null=True, on_delete=models.CASCADE,
                                default='', related_name='hotels', verbose_name='Страна')
    city = models.ForeignKey(City, auto_created=True, null=True, on_delete=models.CASCADE,
                             default='', related_name='hotels', verbose_name='Город')
    description = models.TextField(max_length=2000, default='', verbose_name='Описание')
    category = models.PositiveSmallIntegerField(null=True, verbose_name='Категория')
    is_repair = models.BooleanField(default=False, verbose_name='Недавно отремонтирован')
    service = models.ManyToManyField(Service, related_name='services', verbose_name='Сервис')
    logo = models.ImageField(upload_to='hotels/list', blank=True, null=True, verbose_name='Загрузить изображение')
    objects = EventQuerySet.as_manager()

    @property
    def logo_url(self):
        return self.logo.url if self.logo else f'{settings.STATIC_URL}images/hotels/s1200.jpg'

    def get_absolute_url(self):
        return reverse('hotels:hotel_detail', args=[str(self.pk)])

    def get_update_url(self):
        return reverse('hotels:hotel_update', args=[str(self.pk)])

    def get_delete_url(self):
        return reverse('hotels:hotel_delete', args=[str(self.pk)])

    def __str__(self):
        return f'{self.title}, {self.category}'

    class Meta:
        verbose_name_plural = 'Отели'
        verbose_name = 'Отель'

    @property
    def display_rooms_count(self):
        return self.rooms.count()

    @property
    def display_reviews_count(self):
        reviews_count = self.reviews.values_list('rate', flat=True).count()
        return reviews_count

    @property
    def new_rate(self):
        sum_rate =sum(list(self.reviews.values_list('rate', flat=True)), start=0)
        if self.display_reviews_count > 0:
            new_rate = (sum_rate * 10 / self.display_reviews_count) * 0.1
        else:
            new_rate = sum_rate
        return new_rate

    @property
    def display_booking_count(self):
        booking = 0
        list = self.rooms.values_list('is_booking', flat=True)
        for book in list:
            if book == True:
                booking += 1
        return booking

    @property
    def display_available_count(self):
        return self.display_rooms_count - self.display_booking_count

    @property
    def get_rate(self):
        review = Review.objects.filter(hotel=self).values_list('rate', flat=True).last()
        list = review if review else None
        return list

    @property
    def get_min_price(self):
        list_price = self.rooms.values_list('price', flat=True)
        if list_price.count() == 0:
            min_price = 0
        else:
            min_price = round(min(list_price) / 1000, 3)
        return toFixed(min_price, 3)

    # @property
    def count_rate(self):
        query_set_ratings = self.reviews.values_list('rate', flat=True)
        if query_set_ratings.count() == 0:
            rates = 0
        else:
            rates = sum(query_set_ratings) / query_set_ratings.count()
        return round(rates, 1)


class Room(models.Model):
    ROOM_CLASS_ECONOMY = 'эконом'
    ROOM_CLASS_COMFORT = 'комфорт'
    ROOM_CLASS_JUNIOR_SUITE = 'люкс'
    ROOM_CLASS_SUITE = 'полулюкс'

    ROOM_CLASS_CHOICES = (
        (ROOM_CLASS_ECONOMY, 'эконом'),
        (ROOM_CLASS_COMFORT, 'комфорт'),
        (ROOM_CLASS_JUNIOR_SUITE, 'люкс'),
        (ROOM_CLASS_SUITE, 'полулюкс'),
    )

    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE, related_name='rooms')
    price = models.FloatField(null=True, verbose_name='Цена за ночь')
    category = models.CharField(max_length=10, null=True, choices=ROOM_CLASS_CHOICES, default=ROOM_CLASS_COMFORT,
                                verbose_name='Тип номера')
    description = models.TextField(max_length=1000, default='', verbose_name='Описание')
    logo = models.ImageField(upload_to='rooms/list', blank=True, null=True, verbose_name='Фотография номера')
    is_booking = models.BooleanField(default=False, verbose_name='Забронирована')

    @property
    def logo_url(self):
        return self.logo.url if self.logo else f'{settings.STATIC_URL}images/rooms/room1.jpg'

    def get_absolute_url(self):
        return reverse('hotels:hotel_detail', args=[str(self.hotel.pk)])

    @property
    def get_price_1000(self):
        return self.price / 1000

    @property
    def get_booking_last(self):
        booking_last = Booking.objects.filter(room=self).values_list('pk', flat=True).order_by('date_start').last()
        return booking_last

    def __str__(self):
        return f'{self.pk}: {self.category} - {self.hotel}'

    class Meta:
        verbose_name_plural = 'Номера'
        verbose_name = 'Номер'


class Review(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='reviews')
    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE, related_name='reviews')
    rate = models.PositiveSmallIntegerField(null=True, verbose_name='Оценка пользователя')
    text = models.TextField(verbose_name='Текст отзыва')
    created = models.DateField(verbose_name='Дата отзыва')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'

    def __str__(self):
        return f'{self.user} - {self.hotel} - {self.rate}'

    @property
    def list_rate(self):
        return list('*' * int(self.rate))


class Booking(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='bookings', default=1)
    room = models.ForeignKey(Room, null=True, on_delete=models.CASCADE, related_name='bookings', default=None)
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания')

    def __str__(self):
        return f'{self.room} - {self.user}'

    def get_absolute_url(self):
        return reverse('hotels:room_update', args=[str(self.room.pk)])

    class Meta:
        verbose_name_plural = 'Брони'
        verbose_name = 'Бронь'
