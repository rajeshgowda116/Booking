from decimal import Decimal

from django.core.management.base import BaseCommand

from booking.models import Hotel, Room


class Command(BaseCommand):
    help = 'Create sample hotels and rooms for demonstration.'

    def handle(self, *args, **options):
        hotels = [
            {
                'name': 'Grand Palace Hotel',
                'location': 'Bengaluru',
                'description': 'A comfortable city hotel close to shopping areas, business centers, and local attractions.',
                'contact_number': '+91 98765 43210',
                'email': 'info@grandpalace.example',
                'rating': Decimal('4.5'),
            },
            {
                'name': 'Ocean View Hotel',
                'location': 'Mangaluru',
                'description': 'A relaxed coastal hotel with bright rooms, friendly service, and easy beach access.',
                'contact_number': '+91 98765 43211',
                'email': 'stay@oceanview.example',
                'rating': Decimal('4.3'),
            },
            {
                'name': 'Green Valley Resort',
                'location': 'Mysuru',
                'description': 'A peaceful resort surrounded by greenery, ideal for family vacations and weekend stays.',
                'contact_number': '+91 98765 43212',
                'email': 'hello@greenvalley.example',
                'rating': Decimal('4.6'),
            },
        ]

        room_templates = [
            ('101', Room.SINGLE, Decimal('2000.00'), 1, 'Wi-Fi, AC, TV, Breakfast'),
            ('102', Room.DOUBLE, Decimal('3200.00'), 2, 'Wi-Fi, AC, TV, Breakfast, Workspace'),
            ('201', Room.DELUXE, Decimal('4500.00'), 3, 'Wi-Fi, AC, Smart TV, Mini Fridge, Balcony'),
            ('301', Room.SUITE, Decimal('7000.00'), 4, 'Wi-Fi, AC, Living Area, Bathtub, Premium Breakfast'),
        ]

        for hotel_data in hotels:
            hotel, _ = Hotel.objects.get_or_create(name=hotel_data['name'], defaults=hotel_data)
            for room_number, room_type, price, capacity, facilities in room_templates:
                Room.objects.get_or_create(
                    hotel=hotel,
                    room_number=room_number,
                    defaults={
                        'room_type': room_type,
                        'price_per_night': price,
                        'capacity': capacity,
                        'facilities': facilities,
                        'description': f'A clean and comfortable {room_type.lower()} room with modern facilities.',
                    },
                )

        self.stdout.write(self.style.SUCCESS('Sample hotels and rooms are ready.'))
