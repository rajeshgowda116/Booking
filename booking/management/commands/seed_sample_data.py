from decimal import Decimal
from pathlib import Path
import re
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw

from booking.models import Hotel, Room


def save_image_from_url_or_fallback(url, target_path, label):
    """Save an image from URL if available, or generate a fallback image."""
    target_path = Path(target_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.exists() and target_path.stat().st_size > 1000:
        return True

    downloaded = False
    if url:
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    data = resp.read()
                    target_path.write_bytes(data)
                    downloaded = True
        except Exception:
            downloaded = False

    if not downloaded:
        img = Image.new('RGB', (800, 500), color=(30, 41, 59))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(20, 20), (780, 480)], outline=(255, 193, 7), width=3)
        draw.text((40, 230), label, fill=(255, 255, 255))
        img.save(target_path, format='JPEG', quality=85)

    return True


class Command(BaseCommand):
    help = 'Create sample hotels and rooms with photos for demonstration.'

    def handle(self, *args, **options):
        hotels = [
            {
                'name': 'Grand Palace Hotel',
                'location': 'Bengaluru',
                'description': 'A comfortable city hotel close to shopping areas, business centers, and local attractions.',
                'contact_number': '+91 98765 43210',
                'email': 'info@grandpalace.example',
                'rating': Decimal('4.5'),
                'image_url': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=1200&q=80',
                'rooms': [
                    ('101', Room.SINGLE, Decimal('2000.00'), 10, 'Wi-Fi, AC, TV, Breakfast', 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=1200&q=80'),
                    ('102', Room.DOUBLE, Decimal('3200.00'), 10, 'Wi-Fi, AC, TV, Breakfast, Workspace', 'https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=1200&q=80'),
                    ('201', Room.DELUXE, Decimal('4500.00'), 10, 'Wi-Fi, AC, Smart TV, Mini Fridge, Balcony', 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=80'),
                    ('301', Room.SUITE, Decimal('7000.00'), 10, 'Wi-Fi, AC, Living Area, Bathtub, Premium Breakfast', 'https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=1200&q=80'),
                ],
            },
            {
                'name': 'Ocean View Hotel',
                'location': 'Mangaluru',
                'description': 'A relaxed coastal hotel with bright rooms, friendly service, and easy beach access.',
                'contact_number': '+91 98765 43211',
                'email': 'stay@oceanview.example',
                'rating': Decimal('4.3'),
                'image_url': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?auto=format&fit=crop&w=1200&q=80',
                'rooms': [
                    ('101', Room.SINGLE, Decimal('2000.00'), 10, 'Wi-Fi, AC, TV, Breakfast', 'https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=1200&q=80'),
                    ('102', Room.DOUBLE, Decimal('3200.00'), 10, 'Wi-Fi, AC, TV, Breakfast, Workspace', 'https://images.unsplash.com/photo-1566665797739-1674de7a421a?auto=format&fit=crop&w=1200&q=80'),
                    ('201', Room.DELUXE, Decimal('4500.00'), 10, 'Wi-Fi, AC, Smart TV, Mini Fridge, Balcony', 'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=1200&q=80'),
                    ('301', Room.SUITE, Decimal('7000.00'), 10, 'Wi-Fi, AC, Living Area, Bathtub, Premium Breakfast', 'https://images.unsplash.com/photo-1591088398332-8a7791972843?auto=format&fit=crop&w=1200&q=80'),
                ],
            },
            {
                'name': 'Green Valley Resort',
                'location': 'Mysuru',
                'description': 'A peaceful resort surrounded by greenery, ideal for family vacations and weekend stays.',
                'contact_number': '+91 98765 43212',
                'email': 'hello@greenvalley.example',
                'rating': Decimal('4.6'),
                'image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=1200&q=80',
                'rooms': [
                    ('101', Room.SINGLE, Decimal('2000.00'), 10, 'Wi-Fi, AC, TV, Breakfast', 'https://images.unsplash.com/photo-1598928506311-c55ded91a20c?auto=format&fit=crop&w=1200&q=80'),
                    ('102', Room.DOUBLE, Decimal('3200.00'), 10, 'Wi-Fi, AC, TV, Breakfast, Workspace', 'https://images.unsplash.com/photo-1590490359683-658d3d23f972?auto=format&fit=crop&w=1200&q=80'),
                    ('201', Room.DELUXE, Decimal('4500.00'), 10, 'Wi-Fi, AC, Smart TV, Mini Fridge, Balcony', 'https://images.unsplash.com/photo-1613545325278-f24b0cae1224?auto=format&fit=crop&w=1200&q=80'),
                    ('301', Room.SUITE, Decimal('7000.00'), 10, 'Wi-Fi, AC, Living Area, Bathtub, Premium Breakfast', 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80'),
                ],
            },
        ]

        for hotel_info in hotels:
            hotel_name = hotel_info['name']
            hotel_slug = re.sub(r'[^a-zA-Z0-9]+', '_', hotel_name.lower()).strip('_')
            hotel_img_rel = f'hotels/{hotel_slug}.jpg'
            hotel_img_path = settings.MEDIA_ROOT / hotel_img_rel
            save_image_from_url_or_fallback(hotel_info['image_url'], hotel_img_path, hotel_name)

            hotel_defaults = {
                'location': hotel_info['location'],
                'description': hotel_info['description'],
                'contact_number': hotel_info['contact_number'],
                'email': hotel_info['email'],
                'rating': hotel_info['rating'],
                'image': hotel_img_rel,
            }

            hotel, _ = Hotel.objects.get_or_create(name=hotel_name, defaults=hotel_defaults)
            hotel.image = hotel_img_rel
            hotel.save()

            for room_number, room_type, price, capacity, facilities, room_img_url in hotel_info['rooms']:
                room_img_rel = f'rooms/{hotel_slug}_{room_number}.jpg'
                room_img_path = settings.MEDIA_ROOT / room_img_rel
                save_image_from_url_or_fallback(
                    room_img_url,
                    room_img_path,
                    f'{hotel_name} - {room_type} {room_number}',
                )

                room, _ = Room.objects.get_or_create(
                    hotel=hotel,
                    room_number=room_number,
                    defaults={
                        'room_type': room_type,
                        'price_per_night': price,
                        'capacity': capacity,
                        'facilities': facilities,
                        'description': f'A clean and comfortable {room_type.lower()} room with modern facilities.',
                        'image': room_img_rel,
                    },
                )
                room.image = room_img_rel
                room.room_type = room_type
                room.price_per_night = price
                room.capacity = capacity
                room.facilities = facilities
                room.description = f'A clean and comfortable {room_type.lower()} room with modern facilities.'
                room.save()

        self.stdout.write(self.style.SUCCESS('Sample hotels and rooms with photos are ready.'))
