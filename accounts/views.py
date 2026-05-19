from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile

# 1. Home View
def home(request):
    if request.user.is_authenticated:
        if not request.user.userprofile.is_verified:
            return redirect('verify_payment')
        return redirect('dashboard')
        
    return render(request, 'accounts/home.html') 

# 2. Registration View (Handles form submissions and saves Phone Numbers)
def register(request):
    # Grab the referral code if someone used a referral link, or leave it blank
    ref_code = request.GET.get('ref', '') 
    
    if request.method == 'POST':
        # Extract inputs from the registration form
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')  # Capture the new phone input
        password = request.POST.get('password')
        ref = request.POST.get('ref')

        # Check if username or email already exist to prevent crash errors
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'accounts/register.html', {'ref_code': ref})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'accounts/register.html', {'ref_code': ref})

        # Create core Django user account
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.save()

        # Create the custom UserProfile with phone number and verification status
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            referral_code=ref,  # <-- FIXED: Matched to referral_code in models.py
            is_verified=False   # User must pay 119 KSh to turn this True
        )

        # Log the newly registered user in automatically behind the scenes
        login(request, user)

        # Redirect straight to payment collection
        return redirect('verify_payment')

    # If it's a normal page visit (GET), just display the empty registration page
    context = {
        'ref_code': ref_code
    }
    return render(request, 'accounts/register.html', context)

# 3. Earning Dashboard View
@login_required
def dashboard(request):
    profile = request.user.userprofile
    
    if not profile.is_verified:
        return redirect('verify_payment')
        
    return render(request, 'accounts/dashboard.html', {
        'profile': profile
    })

# 4. Payment Verification View (Passes profile details to checkout template)
@login_required
def verify_payment(request):
    profile = request.user.userprofile
    
    if profile.is_verified:
        return redirect('dashboard')
        
    if request.method == 'POST':
        # 1. Grab the phone number they typed into the confirmation box
        submitted_phone = request.POST.get('phone_number')
        
        # 2. Update their profile with the payment reference phone number
        profile.phone_number = submitted_phone
        profile.save()
        
        # 3. Add a success banner message telling them you are reviewing it
        messages.success(request, f"Payment submission received for {submitted_phone}. Your account will be activated once confirmed.")
        
        # Keep them on the page showing the confirmation message, or redirect as needed
        return redirect('verify_payment')

    return render(request, 'accounts/verify_payment.html', {
        'profile': profile
    })