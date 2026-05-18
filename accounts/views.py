from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# --- ADD THIS HOME VIEW ---
def home(request):
    # If a user is logged in, you might want to redirect them straight to verification or dashboard
    if request.user.is_authenticated:
        if not request.user.userprofile.is_verified:
            return redirect('verify_payment')
        return render(request, 'accounts/dashboard.html') # Or wherever your logged-in users go
        
    # If they are a guest/not logged in, show them the index/landing page
    return render(request, 'accounts/home.html') 


@login_required
def verify_payment(request):
    profile = request.user.userprofile
    
    if profile.is_verified:
        return redirect('dashboard')  # Make sure you have a path named 'dashboard' in urls.py if using this

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        profile.phone_number = phone_number
        profile.save()
        
        return render(request, 'accounts/verification_pending.html', {
            'phone_number': phone_number
        })

    return render(request, 'accounts/verify_payment.html')