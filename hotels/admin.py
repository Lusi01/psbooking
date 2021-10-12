from django.contrib import admin
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'countryname', ]
    fields = ['countryname', 'logo', ]


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'cityname', 'country', ]
    fields = ['cityname', 'country', ]


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', ]
    fields = ['title', ]


class RoomInstanceInline(admin.TabularInline):
    model = models.Room
    fields = ['id', 'hotel', 'price', 'category', 'description', 'is_booking', ]
    extra = 0

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class BookingInstanceInline(admin.TabularInline):
    model = models.Booking
    fields = ['id', 'user', 'date_start', 'date_end', ]
    extra = 0

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class ReviewInstanceInline(admin.TabularInline):
    model = models.Review
    fields = ['id', 'user', 'hotel', 'rate', 'text', 'created', 'updated', ]
    readonly_fields = ['id', 'user', 'hotel', 'rate', 'text', 'created', 'updated', ]
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'city', 'country', 'description', 'category', 'is_repair', 'logo', ]
    list_editable = ['city', 'country', ]
    fields = ['title', 'city', 'country', 'description', 'category', 'is_repair', 'service', 'logo', ]

    def description_input(self, request, obj=None):
        pass

    editable = True
    inlines = [RoomInstanceInline]


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'hotel', 'price', 'category', 'description', 'is_booking', ]
    fields = ['hotel', 'price', 'category', 'description', 'logo', 'is_booking', ]
    inlines = [BookingInstanceInline]


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'date_start', 'date_end', ]
    fields = ['user', 'room', 'date_start', 'date_end', ]
    list_display_links = ['id', 'room', 'user', ]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'hotel', 'rate', 'text', 'created', 'updated', ]
    list_display_links = ['id', 'user', 'hotel', ]
    fields = ['user', 'hotel', 'rate', 'text', 'created', 'updated', 'id']
    readonly_fields = ['id', 'updated']
    list_filter = ['created', 'hotel', ]
