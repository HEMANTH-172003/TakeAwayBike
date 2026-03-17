from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
import math
from .models import *
from authen.models import *

# Create your views here.
def home(request):
    data = Bike.objects.all()
    return render(request,'home.html',{'data':data})

# ----------------------------------------------------------------------------------------
@login_required
def bookings(request,id):
    bike = get_object_or_404(Bike, id=id)
    user = request.user

    profile = Register.objects.get(user=user)  # for mobile

    if request.method == 'POST':
        location = request.POST.get('location')
        date = request.POST.get('date')

        Booking.objects.create(
            user=user,
            bike=bike,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            mobile=profile.mobile,
            bike_image=bike.bike_image,
            exact_location=location,
            booking_date=date
        )

        return redirect('home')

    return render(request, 'bookings.html', {
        'bike': bike,
        'profile': profile
    })

#-----------------------------------------------------------------------------------
@login_required
def contact(request):
    user = request.user
    profile = Register.objects.get(user=user)

    if request.method == 'POST':
        bike_count = int(request.POST.get('bike_count'))
        address = request.POST.get('address')

        # 💰 Calculate advance
        advance_amount = bike_count * 150

        ContactRequest.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            mobile=profile.mobile,
            bike_count=bike_count,
            address=address,
            advance_amount=advance_amount
        )

        return redirect('home')

    return render(request, 'contact.html', {'profile': profile})

#----------------------------------------------------------------------------------
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'my_bookings.html', {
        'bookings': bookings
    })

#-----------------------------------------------------------------------------
def about(request):
    return render(request,'about.html')

#------------------------------------------------------------------
@login_required
def cancelbooking(request, id):
    booking = get_object_or_404(Booking, id=id, user=request.user)

    if request.method == 'POST':
        reason = request.POST.get('reason')

        # Save cancel record
        CancelBooking.objects.create(
            user=request.user,
            booking=booking,
            reason=reason
        )

        # Update booking status
        booking.status = 'Cancelled'
        booking.save()

        return redirect('my_bookings')

    return render(request, 'cancelbooking.html', {'booking': booking})

#-------------------------------------------------------------------------------------
@login_required
def completebooking(request, id):
    booking = get_object_or_404(Booking, id=id, user=request.user)

    start_time = booking.created_at
    end_time = timezone.now()

    # ⏱ Calculate duration
    duration = end_time - start_time
    total_hours = duration.total_seconds() / 3600

    # 🔥 Round up (important)
    total_hours = math.ceil(total_hours)

    # 💰 Amount calculation
    amount_per_hour = booking.bike.amount_per_hour
    total_amount = total_hours * amount_per_hour

    # Save
    completed = CompletedBooking.objects.create(
        user=request.user,
        booking=booking,
        bike=booking.bike,

        first_name=booking.first_name,
        mobile=booking.mobile,

        bike_model=booking.bike.bike_model,
        bike_number=booking.bike.bike_number,
        bike_image=booking.bike.bike_image,
        amount_per_hour=amount_per_hour,

        start_time=start_time,
        end_time=end_time,

        total_hours=total_hours,
        total_amount=total_amount
    )

    booking.status = 'Completed'
    booking.save()

    return render(request, 'completedbill.html', {'c': completed})

#----------------------------------------------------------------------------------------
@login_required
def completedrides(request):
    completed = CompletedBooking.objects.filter(user=request.user).order_by('-completed_at')

    return render(request, 'completedrides.html', {
        'completed': completed
    })

