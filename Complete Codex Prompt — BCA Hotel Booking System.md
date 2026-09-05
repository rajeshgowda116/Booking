# Build a Complete BCA Mini Project: Online Hotel Room Booking System

You are working directly inside my project repository.

I need you to build a complete, working **BCA Mini Project** called:

**Online Hotel Room Booking System**

The goal is to create a simple, professional, user-friendly web application where users can view hotels and rooms, check room availability for specific dates, select a room, and make a booking.

The project must be suitable for a **BCA college mini project**, so keep the architecture simple, understandable, and maintainable. Do not over-engineer it.

---

# 1. Technology Stack

Use:

- Python 3
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Bootstrap 5

Use Django's built-in authentication system.

Do NOT introduce React, Node.js, MongoDB, PostgreSQL, Docker, Redis, Celery, microservices, or unnecessary third-party packages unless absolutely required.

The application should run locally using:

```bash
python manage.py runserver
```

---

# 2. First: Inspect the Repository

Before making changes:

1. Inspect the existing repository.
2. Determine whether a Django project already exists.
3. Check existing files and dependencies.
4. Reuse existing code if appropriate.
5. Do not unnecessarily delete working code.
6. If the repository is empty, create the Django project from scratch.
7. If there is already a project, adapt it instead of creating a duplicate project.

After inspection, determine the appropriate project structure and proceed.

Do not just tell me what to do. **Actually create and modify the files in the repository.**

---

# 3. Project Requirements

The system has two main roles:

## User

Users should be able to:

- Register
- Login
- Logout
- View hotels
- Search hotels
- View hotel details
- View available rooms
- View room details
- Select check-in date
- Select check-out date
- Select number of guests
- Check room availability
- Book a room
- View booking confirmation
- View their booking history
- Cancel eligible bookings

## Admin

Use Django Admin.

Admin should be able to:

- Login
- Add hotels
- Edit hotels
- Delete hotels
- Add rooms
- Edit rooms
- Delete rooms
- View users
- View bookings
- Change booking status

---

# 4. Main Database Models

Create these models:

```text
User
Hotel
Room
Booking
```

Use Django's built-in User model unless there is a strong reason to create a custom user model.

---

# 5. Hotel Model

Create a Hotel model containing approximately:

- name
- location
- description
- image
- contact_number
- email
- rating
- created_at

Use appropriate Django field types and validation.

The image should use Django media storage.

---

# 6. Room Model

Create a Room model containing:

- hotel
- room_number
- room_type
- price_per_night
- capacity
- description
- facilities
- image
- created_at

Room types:

- Single
- Double
- Deluxe
- Suite

Use a ForeignKey from Room to Hotel.

A hotel can have multiple rooms.

---

# 7. Booking Model

Create a Booking model containing:

- user
- room
- check_in
- check_out
- number_of_guests
- number_of_nights
- total_amount
- booking_date
- status

Booking statuses:

- Confirmed
- Cancelled
- Completed

Use proper relationships.

---

# 8. Critical Booking Availability Logic

This is one of the most important requirements.

A room must NOT be booked if another confirmed booking overlaps with the requested dates.

Use the standard overlap condition:

```python
existing_booking.check_in < requested_check_out
and
existing_booking.check_out > requested_check_in
```

In Django query form, use the equivalent logic:

```python
Booking.objects.filter(
    room=room,
    status="Confirmed",
    check_in__lt=check_out,
    check_out__gt=check_in
).exists()
```

If this returns True:

```text
Room is NOT available.
```

If False:

```text
Room is available.
```

Do not rely on a simple boolean field such as:

```text
room.available = True
```

because room availability depends on the selected dates.

Also prevent race-condition-like duplicate bookings as far as practical within this simple SQLite/Django project.

---

# 9. Booking Validation

Before creating a booking, validate:

### Check-in

Check-in cannot be in the past.

### Check-out

Check-out must be after check-in.

Example:

```text
Check-in: 10 September
Check-out: 15 September

Valid
```

But:

```text
Check-in: 15 September
Check-out: 10 September

Invalid
```

### Guests

Number of guests must be greater than zero.

Number of guests cannot exceed room capacity.

### Room availability

The selected room must be available for the requested date range.

If unavailable, do not create the booking.

Show a clear user-friendly error.

---

# 10. Price Calculation

Calculate:

```text
number_of_nights =
check_out - check_in
```

Then:

```text
total_amount =
number_of_nights × room.price_per_night
```

Example:

```text
Price per night = ₹2000
Number of nights = 3

Total = ₹6000
```

Do not trust a price submitted by the browser.

Calculate the price on the server using the database room price.

Use DecimalField for monetary values.

---

# 11. Required Pages

Create the following pages.

## Public pages

```text
/
```

Home page.

```text
/hotels/
```

Hotel listing.

```text
/hotels/<id>/
```

Hotel details.

```text
/rooms/<id>/
```

Room details.

```text
/login/
```

Login.

```text
/register/
```

Registration.

---

## Authenticated pages

```text
/booking/<room_id>/
```

Booking form.

```text
/booking/<booking_id>/confirmation/
```

Booking confirmation.

```text
/my-bookings/
```

User booking history.

```text
/booking/<booking_id>/cancel/
```

Cancel booking.

Use appropriate URL names and Django best practices.

---

# 12. Home Page UI

Create a professional but simple homepage.

Include:

### Navbar

```text
Hotel Booking
Home
Hotels
My Bookings
Login/Register
```

If the user is logged in:

```text
Welcome, username
My Bookings
Logout
```

### Hero section

Include a large heading such as:

```text
Find Your Perfect Stay
```

And a short description.

Include a hotel search form.

### Featured Hotels

Display several hotel cards.

Each card should include:

- Hotel image
- Hotel name
- Location
- Rating
- Short description
- View Details button

### Footer

Include:

- Project name
- Short description
- Copyright
- Useful links

---

# 13. Hotel Listing Page

Display hotels in responsive Bootstrap cards.

Each card should contain:

- Image
- Name
- Location
- Rating
- Description
- View Rooms button

Add a search box.

Users should be able to search by:

- Hotel name
- Location

Use Django query filtering.

---

# 14. Hotel Details Page

Display:

- Hotel image
- Hotel name
- Location
- Rating
- Description
- Contact information

Below it, display rooms belonging to the hotel.

Each room card should contain:

```text
Room image
Room type
Price per night
Capacity
Facilities
View Details
Book Now
```

---

# 15. Room Details Page

Display detailed room information:

- Room image
- Hotel name
- Room type
- Room number
- Price per night
- Capacity
- Facilities
- Description

Provide:

```text
Book This Room
```

button.

---

# 16. Booking Page

The booking form should contain:

```text
Room
Check-in date
Check-out date
Number of guests
```

Show room information on the page.

After submission:

1. Validate the form.
2. Validate dates.
3. Validate guest count.
4. Check availability.
5. Calculate number of nights.
6. Calculate total amount.
7. Create booking.
8. Redirect to confirmation page.

If anything fails, show a clear error message.

---

# 17. Booking Confirmation Page

After successful booking, display:

```text
Booking Confirmed

Booking ID
Customer Name
Hotel Name
Room Type
Room Number
Check-in Date
Check-out Date
Number of Guests
Number of Nights
Price Per Night
Total Amount
Booking Status
Booking Date
```

Make this page visually clean.

Add:

```text
View My Bookings
Back to Home
```

buttons.

---

# 18. My Bookings Page

Only authenticated users can access this page.

Display only the current user's bookings.

Show:

```text
Booking ID
Hotel
Room
Check-in
Check-out
Guests
Total Amount
Status
Actions
```

For eligible bookings, provide:

```text
Cancel Booking
```

Do not allow one user to access another user's booking through changing an ID in the URL.

Always verify ownership.

---

# 19. Booking Cancellation

Allow users to cancel their own confirmed bookings when appropriate.

When cancelled:

```text
status = Cancelled
```

Do not delete the booking record.

Keep it for booking history.

Do not allow already cancelled bookings to be cancelled again.

Do not allow completed bookings to be cancelled.

Use POST requests for cancellation rather than GET requests.

---

# 20. Authentication

Use Django authentication.

Implement:

### Registration

Fields:

```text
Username
Email
Password
Confirm Password
```

Validate:

- Username uniqueness
- Email format
- Password confirmation
- Password requirements

### Login

Use Django authentication.

### Logout

Use Django logout.

Protect booking-related pages with:

```python
@login_required
```

---

# 21. Admin Panel

Register all relevant models in Django Admin.

Customize the admin interface with:

### HotelAdmin

Display:

```text
name
location
rating
created_at
```

### RoomAdmin

Display:

```text
room_number
hotel
room_type
price_per_night
capacity
```

### BookingAdmin

Display:

```text
id
user
room
check_in
check_out
number_of_guests
total_amount
status
booking_date
```

Add useful filters and search fields.

---

# 22. Templates

Use a common:

```text
base.html
```

Use Django template inheritance.

Suggested structure:

```text
templates/
    booking/
        base.html
        home.html
        hotels.html
        hotel_detail.html
        room_detail.html
        booking_form.html
        booking_confirmation.html
        my_bookings.html
        login.html
        register.html
```

Do not duplicate the navbar and footer in every file.

---

# 23. Static Files

Create:

```text
static/
    booking/
        css/
            style.css
        js/
            script.js
```

Use Bootstrap 5.

The application must be responsive on:

- Desktop
- Tablet
- Mobile

---

# 24. Media Files

Configure Django media handling.

Use:

```python
MEDIA_URL
MEDIA_ROOT
```

During development, configure media serving correctly through Django URLs.

If an image is missing, display a reasonable placeholder or fallback.

---

# 25. UI Design

Make the application look like a real hotel booking website.

Design requirements:

- Clean layout
- Professional typography
- Consistent spacing
- Responsive cards
- Attractive hotel images
- Clear buttons
- Bootstrap alerts
- Good form design
- Mobile-friendly navbar
- Simple footer

Do not make the UI excessively complicated.

The project should look professional enough for a BCA demonstration.

---

# 26. Error Handling

Handle common errors gracefully:

- Invalid hotel ID
- Invalid room ID
- Invalid booking ID
- Unauthorized booking access
- Invalid dates
- Unavailable room
- Invalid number of guests
- Missing images
- Empty search results

Use Django's:

```text
get_object_or_404()
```

where appropriate.

Show user-friendly error messages.

---

# 27. Security Requirements

Follow Django security best practices.

Use:

- CSRF protection
- Django password hashing
- Authentication
- Authorization
- POST for state-changing operations
- Server-side validation
- User ownership checks

Do not expose sensitive information.

Do not store plain-text passwords.

Do not trust values such as total price sent by the client.

---

# 28. Database and Migrations

Create and run migrations.

Use:

```bash
python manage.py makemigrations
python manage.py migrate
```

Make sure the database works correctly.

---

# 29. Sample Data

Create a simple way to populate sample data for demonstration.

Include sample hotels such as:

```text
Grand Palace Hotel
Location: Bengaluru

Ocean View Hotel
Location: Mangaluru

Green Valley Resort
Location: Mysuru
```

Create multiple rooms for each hotel.

Example room types:

```text
Single
Double
Deluxe
Suite
```

Use realistic sample prices and capacities.

If images cannot be automatically downloaded, make the application work without them and provide a clear way to add images manually through Django Admin.

---

# 30. Sample Booking Test

After implementation, test:

```text
Room 101
Price: ₹2000/night

Booking:
10 September → 15 September

Nights = 5

Total = ₹10000
```

Then attempt:

```text
12 September → 14 September
```

This should fail because the dates overlap.

Then attempt:

```text
16 September → 20 September
```

This should succeed.

---

# 31. Automated Tests

Create Django tests for important functionality.

At minimum test:

### Registration

- Successful registration
- Password mismatch

### Authentication

- Login
- Invalid login

### Booking

- Successful booking
- Overlapping booking rejected
- Invalid date rejected
- Past check-in rejected
- Guests exceeding capacity rejected
- Correct total amount

### Authorization

- User cannot access another user's booking
- Anonymous user cannot access protected booking pages

### Cancellation

- Confirmed booking can be cancelled
- Cancelled booking cannot be cancelled again

Run:

```bash
python manage.py test
```

Fix all test failures.

---

# 32. Code Quality

Follow Django conventions.

Use:

- Meaningful names
- Small functions
- Clear model relationships
- Form validation where appropriate
- Comments only where useful
- No unnecessary duplication

Do not put all business logic into templates.

Keep the code understandable for a BCA student.

---

# 33. README

Create a complete README.md containing:

```text
Project Title
Project Description
Features
Technology Stack
Project Structure
Installation
Virtual Environment Setup
Dependency Installation
Database Migration
Create Superuser
Run Development Server
Admin Login
Sample Data
Testing
Future Enhancements
```

Include exact commands.

For example:

```bash
python -m venv venv
```

Windows activation:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install django pillow
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create admin:

```bash
python manage.py createsuperuser
```

Run:

```bash
python manage.py runserver
```

Only include commands that match the actual project.

---

# 34. requirements.txt

Create a requirements.txt containing the actual dependencies used by the project.

Do not add unused packages.

---

# 35. Development Process

Work on the project in the following order:

## Phase 1 — Inspect and Setup

- Inspect repository
- Create/configure Django project
- Configure settings
- Configure static/media
- Configure templates
- Configure SQLite

## Phase 2 — Database

- Hotel model
- Room model
- Booking model
- Migrations
- Admin

## Phase 3 — Authentication

- Registration
- Login
- Logout
- Authentication protection

## Phase 4 — Hotel and Room UI

- Homepage
- Hotel listing
- Hotel details
- Room details

## Phase 5 — Booking

- Booking form
- Availability checking
- Date validation
- Guest validation
- Price calculation
- Booking creation
- Confirmation

## Phase 6 — User Dashboard

- My bookings
- Booking details
- Cancellation

## Phase 7 — UI Improvements

- Responsive Bootstrap design
- Error messages
- Alerts
- Navigation
- Footer
- Mobile support

## Phase 8 — Testing

- Run Django checks
- Run migrations
- Run tests
- Start development server
- Fix errors
- Test complete user flow

---

# 36. Important Codex Behavior

You are an implementation agent, not only a coding tutor.

Therefore:

**DO NOT simply give me code in your response.**

Instead:

1. Inspect the repository.
2. Create/edit the necessary files directly.
3. Install only required dependencies.
4. Run Django checks.
5. Run migrations.
6. Run tests.
7. Fix errors you encounter.
8. Re-run tests.
9. Verify the project starts successfully.
10. Review the final project for obvious issues.

If you encounter an error:

```text
Read the error
↓
Identify the cause
↓
Fix the code
↓
Run the relevant command again
↓
Verify the fix
```

Do not stop at the first error.

---

# 37. Do Not Over-Engineer

This is a BCA mini project.

Do NOT add:

- Payment gateway
- AI
- Chatbot
- Recommendation engine
- Complex APIs
- Microservices
- Docker
- Redis
- Celery
- React
- Unnecessary external services

unless I explicitly request them later.

Focus on:

```text
Hotels
    ↓
Rooms
    ↓
Availability
    ↓
Booking
    ↓
Confirmation
    ↓
Booking History
```

---

# 38. Final Acceptance Criteria

Consider the project complete only when all of these work:

### User

```text
Register
↓
Login
↓
View Hotels
↓
View Hotel
↓
View Rooms
↓
View Room
↓
Select Dates
↓
Check Availability
↓
Book Room
↓
Booking Confirmation
↓
View My Bookings
↓
Cancel Booking
```

### Admin

```text
Admin Login
↓
Manage Hotels
↓
Manage Rooms
↓
View Users
↓
Manage Bookings
```

### Technical

```text
Django checks pass
Migrations work
Tests pass
Authentication works
Authorization works
Availability logic works
Price calculation works
Responsive UI works
No obvious broken links
No obvious server errors
```

---

# 39. Final Response After Implementation

Once you have actually implemented and tested the project, give me a concise summary containing:

1. What was created
2. Important files
3. Technologies used
4. Database models
5. Features implemented
6. Tests performed
7. How to run the project
8. Any remaining limitations

Do not claim something is tested unless you actually ran the test or command.

Start by **inspecting the repository now**, then proceed with implementation.