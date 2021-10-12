from django.urls import path
from django.views.decorators.http import require_POST
from . import views

app_name = 'hotels'

urlpatterns = [
    path('list/', views.HotelListView.as_view(), name='hotels_list'),
    path('detail/<int:pk>/', views.HotelDetailView.as_view(), name='hotel_detail'),
    path('city-create/', views.CityCreateView.as_view(), name='city_create'),
    path('city-update/<int:pk>/', views.CityUpdateView.as_view(), name='city_update'),
    path('city-delete/<int:pk>/', views.CityDeleteView.as_view(), name='city_delete'),
    path('hotel-create/', views.HotelCreateView.as_view(), name='hotel_create'),
    path('hotel-update/<int:pk>/', views.HotelUpdateView.as_view(), name='hotel_update'),
    path('room-create/<int:hotel_id>/', views.RoomCreateView.as_view(), name='room_create'),
    path('room-update/<int:pk>/', views.RoomUpdateView.as_view(), name='room_update'),
    path('room-booking/', require_POST(views.RoomBookingView.as_view()), name='room_booking'),
    path('room-unbooking/<int:pk>/', views.room_unbooking, name='room_unbooking'),
    path('review-creation/', require_POST(views.ReviewCreationView.as_view()), name='review_creation'),
]