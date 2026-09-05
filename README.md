# Online Hotel Room Booking System

A complete BCA mini project built with Django. Users can register, log in, browse hotels and rooms, check date-based availability, book rooms, view confirmations, see booking history, and cancel eligible bookings. Admin users can manage hotels, rooms, users, and bookings from Django Admin.

## Features

- User registration, login, and logout
- Hotel search by name or location
- Hotel and room detail pages
- Room booking with check-in, check-out, and guest validation
- Date overlap prevention for confirmed bookings
- Server-side price calculation
- Booking confirmation and booking history
- POST-based booking cancellation
- Django Admin management screens
- Bootstrap 5 responsive interface
- Sample data command
- Automated Django tests

## Technology Stack

- Python 3
- Django 5.2.14
- SQLite
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Pillow for image uploads

## Project Structure

```text
hotelbooking/          Django project settings and URLs
booking/               Main application
booking/models.py      Hotel, Room, Booking models
booking/views.py       Public, auth, and booking views
booking/forms.py       Registration and booking forms
booking/templates/     HTML templates
booking/static/        CSS and JavaScript
booking/management/    Sample data command
README.md
requirements.txt
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Load sample hotels and rooms:

```bash
python manage.py seed_sample_data
```

Run the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin login:

```text
http://127.0.0.1:8000/admin/
```

## Testing

Run automated tests:

```bash
python manage.py test
```

The tests cover registration, login, booking validation, overlap rejection, total calculation, authorization, and cancellation.

## Sample Booking Test

With sample room `101` priced at `₹2000/night`:

- Booking 10 September to 15 September gives 5 nights and total `₹10000`
- A second booking from 12 September to 14 September is rejected because it overlaps
- A later booking from 16 September to 20 September succeeds

## Future Enhancements

- Payment integration
- Email confirmation
- Advanced room filters
- Admin dashboard charts
- Booking invoice PDF
