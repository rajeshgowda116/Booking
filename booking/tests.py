from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Booking, Hotel, Room


class BaseBookingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rajesh', password='StrongPass123', email='rajesh@example.com')
        self.other_user = User.objects.create_user(username='other', password='StrongPass123', email='other@example.com')
        self.hotel = Hotel.objects.create(
            name='Grand Palace Hotel',
            location='Bengaluru',
            description='City hotel',
            contact_number='1234567890',
            email='hotel@example.com',
            rating=Decimal('4.5'),
        )
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number='101',
            room_type=Room.SINGLE,
            price_per_night=Decimal('2000.00'),
            capacity=2,
            description='Nice room',
            facilities='Wi-Fi, AC',
        )


class RegistrationAuthenticationTests(BaseBookingTest):
    def test_successful_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_form_no_help_text(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '150 characters or fewer')
        self.assertNotContains(response, 'too similar to your other personal information')
        self.assertNotContains(response, 'Enter the same password as before')

    def test_password_validation_errors(self):
        response = self.client.post(reverse('register'), {
            'username': 'baduser',
            'email': 'bad@example.com',
            'password1': '123',
            'password2': '123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='baduser').exists())
        self.assertContains(response, 'This password is too short')

    def test_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'baduser',
            'email': 'bad@example.com',
            'password1': 'StrongPass123',
            'password2': 'DifferentPass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='baduser').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'rajesh', 'password': 'StrongPass123'})
        self.assertRedirects(response, reverse('home'))

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {'username': 'rajesh', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password')


class BookingFlowTests(BaseBookingTest):
    def setUp(self):
        super().setUp()
        self.client.login(username='rajesh', password='StrongPass123')
        self.check_in = timezone.localdate() + timedelta(days=5)
        self.check_out = self.check_in + timedelta(days=5)

    def post_booking(self, check_in=None, check_out=None, guests=1):
        return self.client.post(reverse('book_room', args=[self.room.id]), {
            'check_in': check_in or self.check_in,
            'check_out': check_out or self.check_out,
            'number_of_guests': guests,
        })

    def test_successful_booking_and_total_amount(self):
        response = self.post_booking()
        booking = Booking.objects.get()
        self.assertRedirects(response, reverse('booking_confirmation', args=[booking.id]))
        self.assertEqual(booking.number_of_nights, 5)
        self.assertEqual(booking.total_amount, Decimal('10000.00'))

    def test_overlapping_booking_rejected(self):
        Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=self.check_in,
            check_out=self.check_out,
            number_of_guests=1,
            number_of_nights=5,
            total_amount=Decimal('10000.00'),
        )
        response = self.post_booking(check_in=self.check_in + timedelta(days=2), check_out=self.check_in + timedelta(days=4))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertContains(response, 'Room is not available')

    def test_non_overlapping_booking_succeeds(self):
        Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=self.check_in,
            check_out=self.check_out,
            number_of_guests=1,
            number_of_nights=5,
            total_amount=Decimal('10000.00'),
        )
        response = self.post_booking(check_in=self.check_out + timedelta(days=1), check_out=self.check_out + timedelta(days=5))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 2)

    def test_invalid_date_rejected(self):
        response = self.post_booking(check_in=self.check_out, check_out=self.check_in)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)

    def test_past_check_in_rejected(self):
        response = self.post_booking(check_in=timezone.localdate() - timedelta(days=1), check_out=timezone.localdate() + timedelta(days=1))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)

    def test_guests_exceeding_capacity_rejected(self):
        response = self.post_booking(guests=3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)


class AuthorizationCancellationTests(BaseBookingTest):
    def setUp(self):
        super().setUp()
        today = timezone.localdate() + timedelta(days=3)
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=today,
            check_out=today + timedelta(days=2),
            number_of_guests=1,
            number_of_nights=2,
            total_amount=Decimal('4000.00'),
        )

    def test_user_cannot_access_another_users_booking(self):
        self.client.login(username='other', password='StrongPass123')
        response = self.client.get(reverse('booking_confirmation', args=[self.booking.id]))
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_cannot_access_protected_pages(self):
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_confirmed_booking_can_be_cancelled(self):
        self.client.login(username='rajesh', password='StrongPass123')
        response = self.client.post(reverse('cancel_booking', args=[self.booking.id]))
        self.assertRedirects(response, reverse('my_bookings'))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.CANCELLED)

    def test_cancelled_booking_cannot_be_cancelled_again(self):
        self.booking.status = Booking.CANCELLED
        self.booking.save()
        self.client.login(username='rajesh', password='StrongPass123')
        response = self.client.post(reverse('cancel_booking', args=[self.booking.id]))
        self.assertRedirects(response, reverse('my_bookings'))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.CANCELLED)
