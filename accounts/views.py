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
def dashboard(request):
    profile = request.user.userprofile
    
    # If they haven't verified their phone/payment yet, kick them back to the verification page
    if not profile.is_verified:
        return redirect('verify_payment')
        
    # If they are verified, show them the earning dashboard
    return render(request, 'accounts/dashboard.html', {
        'profile': profile
    })