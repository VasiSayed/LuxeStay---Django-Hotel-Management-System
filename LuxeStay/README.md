Luxe Stay Management System

Luxe Stay Management System is a robust web application built with Django to manage residential bookings, tenant details, and admin operations efficiently. The platform is designed to cater to both users (tenants) and hotel administrators (hoteliers) with a seamless experience.

# Features
For Users (Tenants)
- Room Booking: Users can directly book available rooms online through a simple and intuitive panel.
- Residency Search: Search residencies by name, state, or city and filter residencies by price.
- Booking Overview: View current and past bookings in the user dashboard.
- PDF Download: Download booking receipts or confirmations as PDFs.
- Account Management:
  - Forget Password: Recover your account easily.
  - Change Password: Update your account credentials securely.
- Payments: Integrated with Razorpay for secure and seamless payments.
- Email Notifications:
  - Receive emails upon successful registration.
  - Get booking confirmations via email.
For Admins (Hoteliers)
- Residency and Room Management:
  - Create, update, or delete residencies and rooms.
  - Validate room details with full error handling and prevent invalid operations.
  - Disable or delete rooms with future bookings disabled automatically.
  - Option to shut down a room for new bookings where it's already booked.
- No Direct Bookings: Admins cannot make bookings. Booking functionality is exclusively available to users.
- Separate Admin Panel for Hoteliers:
  - Custom admin panel exclusively for hoteliers to manage operations.
  - Overview of monthly and yearly collection and residency statistics.
  - View and count active residencies and rooms.
  - Notifications and reports for room deletions or updates.
- Email Notifications: Receive emails when rooms are deleted or disabled.
Access Control
Secure Admin Pages: Prevent unauthorized users or guests from accessing the hotelier admin panel.


# Tech Stack
- Backend: Django (Python)
- Frontend: HTML, CSS, JavaScript (Bootstrap for styling)
- Database: SQLite / MySQL (configurable as per deployment)
- Payment Gateway: Razorpay integration for online payments.
- PDF Generation: Built-in functionality to generate booking confirmations.
- Email Notifications: SMTP integration for sending user and admin emails.

# Installation
1. Clone the Repository

```bash
git clone https://github.com/VasiSayed/LuxeStay---Django-Hotel-Management-System.git
cd LuxeStay
```
2. Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # For Windows, use env\Scripts\activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Create a Superuser
```bash
python manage.py createsuperuser
```
6. Run the Development Server
```bash
python manage.py runserver
```
7. Open your browser and navigate to `http://127.0.0.1:8000`.


# Usage
For Users:
1. Register for an account.
2. Search for residencies by name, state, or city using the search bar.
3. Filter results by price for the best options.
4. Book available rooms and make payments securely via Razorpay.
5. View booking details, download receipts, and manage your account.
For Admins:
1. Login to the custom admin panel for hoteliers.
2. Manage residencies, rooms, and bookings.
3. Monitor collections and occupancy statistics.


# Directory Structure

luxe_stay/
├── luxe_stay/           # Project settings and configuration
├── main_app/            # Main app for booking and residency management
├── templates/           # HTML templates for frontend
├── static/              # Static files (CSS, JS, images)
├── db.sqlite3           # SQLite database (can be replaced with MySQL)
├── manage.py            # Django management script
├── requirements.txt     # Dependencies


Contributing
Contributions are welcome! Feel free to fork the repository, open issues, or submit pull requests.

Contact
- **Name**: Vasi Sayed
- **Email**: [vasisayed09421@gmail.com]
