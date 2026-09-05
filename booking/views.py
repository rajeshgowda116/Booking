from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Min, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm, RegistrationForm
from .models import Booking, Hotel, Room


def home(request):
    query = request.GET.get('q', '').strip()
    hotels = Hotel.objects.annotate(min_price=Min('rooms__price_per_night'))
    if query:
        hotels = hotels.filter(Q(name__icontains=query) | Q(location__icontains=query))
    return render(request, 'booking/home.html', {'hotels': hotels[:6], 'query': query})


def hotel_list(request):
    query = request.GET.get('q', '').strip()
    hotels = Hotel.objects.annotate(min_price=Min('rooms__price_per_night'))
    if query:
        hotels = hotels.filter(Q(name__icontains=query) | Q(location__icontains=query))
    return render(request, 'booking/hotels.html', {'hotels': hotels, 'query': query})


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    rooms = hotel.rooms.all()
    return render(request, 'booking/hotel_detail.html', {'hotel': hotel, 'rooms': rooms})


def room_detail(request, room_id):
    room = get_object_or_404(Room.objects.select_related('hotel'), pk=room_id)
    return render(request, 'booking/room_detail.html', {'room': room})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'booking/register.html', {'form': form})


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room.objects.select_related('hotel'), pk=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, room=room)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            guests = form.cleaned_data['number_of_guests']
            nights = (check_out - check_in).days

            try:
                with transaction.atomic():
                    locked_room = Room.objects.select_for_update().get(pk=room.pk)
                    if Booking.has_overlap(locked_room, check_in, check_out):
                        messages.error(request, 'Room is not available for the selected dates.')
                    else:
                        booking = Booking.objects.create(
                            user=request.user,
                            room=locked_room,
                            check_in=check_in,
                            check_out=check_out,
                            number_of_guests=guests,
                            number_of_nights=nights,
                            total_amount=locked_room.price_per_night * nights,
                        )
                        messages.success(request, 'Your room has been booked successfully.')
                        return redirect('booking_confirmation', booking_id=booking.pk)
            except Room.DoesNotExist:
                messages.error(request, 'Selected room no longer exists.')
    else:
        form = BookingForm(room=room)
    return render(request, 'booking/booking_form.html', {'form': form, 'room': room})


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related('room__hotel', 'user'),
        pk=booking_id,
        user=request.user,
    )
    return render(request, 'booking/booking_confirmation.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('room__hotel')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method != 'POST':
        messages.error(request, 'Please use the cancel button to cancel a booking.')
        return redirect('my_bookings')

    if booking.status == Booking.CONFIRMED:
        booking.status = Booking.CANCELLED
        booking.save(update_fields=['status'])
        messages.success(request, 'Booking cancelled successfully.')
    elif booking.status == Booking.CANCELLED:
        messages.warning(request, 'This booking is already cancelled.')
    else:
        messages.error(request, 'Completed bookings cannot be cancelled.')
    return redirect('my_bookings')
