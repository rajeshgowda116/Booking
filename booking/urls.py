from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.home, name='home'),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='booking/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('booking/<int:room_id>/', views.book_room, name='book_room'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
