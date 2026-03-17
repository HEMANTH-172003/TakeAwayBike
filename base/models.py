from django.db import models
from authen.models import *

# Create your models here.

class Bike(models.Model):

    bike_image = models.ImageField(upload_to='bike_images/',default='default.jpg')
    bike_number = models.CharField(max_length=20)
    bike_model = models.CharField(max_length=25)

    bike_owner = models.CharField(max_length=100)
    owner_image = models.ImageField(upload_to='owner_images/')

    owner_mobile = models.CharField(max_length=10)
    owner_address = models.TextField()

    location = models.CharField(max_length=200)

    amount_per_hour = models.DecimalField(max_digits=6, decimal_places=2)

    available_from = models.TimeField()
    available_to = models.TimeField()

    is_available = models.BooleanField(default=True)

#------------------------------------------------------------------------------

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey('Bike', on_delete=models.CASCADE)

    # 👤 User Details (auto-filled)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)

    # 🏍 Bike Info (snapshot at booking time)
    bike_image = models.ImageField(upload_to='bookings/', null=True, blank=True)

    # 📍 Booking Details
    exact_location = models.TextField()
    booking_date = models.DateField()

    # 📊 Status Tracking
    STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Booked')

    # ⏱ Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

#-----------------------------------------------------------------------------------

class CancelBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)

    reason = models.TextField(blank=True, null=True)
    cancelled_at = models.DateTimeField(auto_now_add=True)

#-------------------------------------------------------------------------------------------

class CompletedBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    bike = models.ForeignKey('Bike', on_delete=models.CASCADE)

    # 👤 User
    first_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

    # 🏍 Bike
    bike_model = models.CharField(max_length=100)
    bike_number = models.CharField(max_length=50)
    bike_image = models.ImageField(upload_to='completed/', null=True, blank=True)
    amount_per_hour = models.DecimalField(max_digits=8, decimal_places=2)

    # ⏱ Time
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    total_hours = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    completed_at = models.DateTimeField(auto_now_add=True)

#------------------------------------------------------------------------------------

class ContactRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 👤 User details (auto-filled snapshot)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)

    # 🚲 Request details
    bike_count = models.IntegerField()
    address = models.TextField()

    # 💰 Advance amount
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)


    
