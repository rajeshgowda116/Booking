from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('5.0'))],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Room(models.Model):
    SINGLE = 'Single'
    DOUBLE = 'Double'
    DELUXE = 'Deluxe'
    SUITE = 'Suite'

    ROOM_TYPES = [
        (SINGLE, 'Single'),
        (DOUBLE, 'Double'),
        (DELUXE, 'Deluxe'),
        (SUITE, 'Suite'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField()
    facilities = models.TextField(help_text='Comma-separated facilities, such as Wi-Fi, AC, TV')
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['hotel__name', 'room_number']
        unique_together = ('hotel', 'room_number')

    def __str__(self):
        return f'{self.hotel.name} - Room {self.room_number}'


class Booking(models.Model):
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    number_of_nights = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CONFIRMED)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f'Booking #{self.pk} - {self.user.username}'

    @staticmethod
    def has_overlap(room, check_in, check_out, exclude_booking_id=None):
        bookings = Booking.objects.filter(
            room=room,
            status=Booking.CONFIRMED,
            check_in__lt=check_out,
            check_out__gt=check_in,
        )
        if exclude_booking_id:
            bookings = bookings.exclude(pk=exclude_booking_id)
        return bookings.exists()
