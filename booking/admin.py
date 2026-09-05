from django.contrib import admin

from .models import Booking, Hotel, Room


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'created_at')
    search_fields = ('name', 'location', 'email')
    list_filter = ('rating', 'created_at')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hotel', 'room_type', 'price_per_night', 'capacity')
    search_fields = ('room_number', 'hotel__name', 'room_type')
    list_filter = ('room_type', 'capacity', 'hotel')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in', 'check_out', 'number_of_guests', 'total_amount', 'status', 'booking_date')
    search_fields = ('user__username', 'room__room_number', 'room__hotel__name')
    list_filter = ('status', 'check_in', 'booking_date')
    list_editable = ('status',)
