from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,update_session_auth_hash,logout
from .models import *

# Create your views here.
def login_(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')   # change to your home page
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })
    return render(request,'login.html')

#-------------------------------------------------------------------------------------

def register(request):
    if request.method == "POST":

        # ✅ FIRST get values
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        profile_image = request.FILES.get('profile_image')
        document = request.FILES.get('document')

        # ✅ THEN validate username
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        # ✅ Create User
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()

        # ✅ Create Profile
        Register.objects.create(
            user=user,
            mobile=mobile,
            address=address,
            profile_image=profile_image,
            document=document
        )

        return render(request, 'register.html', {
            'success': 'User registered successfully'
        })

    return render(request, 'register.html')

#-----------------------------------------------------------------------------------

def profile(request):
    if request.user.is_authenticated:
        data = Register.objects.get(user = request.user)
        return render(request,'profile.html',{'data':data})
    else:
        return redirect('login_')

#-------------------------------------------------------------------------------------

def logout_(request):
    logout(request)  
    return redirect('home')

#----------------------------------------------------------------------------

def update(request):
    if request.user.is_authenticated:
        profile = Register.objects.get(user=request.user)

        if request.method == "POST":
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.email = request.POST.get('email')
            request.user.save()

            profile.mobile = request.POST.get('mobile')
            profile.address = request.POST.get('address')

            if request.FILES.get('profile_image'):
                profile.profile_image = request.FILES.get('profile_image')

            if request.FILES.get('document'):
                profile.document = request.FILES.get('document')

            profile.save()

            return redirect('profile')

        return render(request, 'update.html', {'data': profile})

    return redirect('login')

#-------------------------------------------------------------------------------

def reset(request):
    if request.method == "POST":
        new_password = request.POST.get('password')

        user = request.user
        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)  # keep user logged in

        return redirect('profile')

    return render(request,'reset.html')

#-------------------------------------------------------------------------

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        new_password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            return redirect('login_')

        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {
                'error': 'User not found'
            })

    return render(request, 'forgot_password.html')