from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
# 1. Home View
def home(request):
    if request.user.is_authenticated:
        if not request.user.userprofile.is_verified:
            return redirect('verify_payment')
        return redirect('dashboard') # Using redirect here keeps things cleaner!
        
    return render(request, 'accounts/home.html') 

def register(request):
    # Grab the referral code if someone used a referral link, or leave it blank
    ref_code = request.GET.get('ref', '') 
    
    context = {
        'ref_code': ref_code
    }
    
    # Send the context dictionary containing 'ref_code' to the template
    return render(request, 'accounts/register.html', context)

# 2. Earning Dashboard View
@login_required
def dashboard(request):
    profile = request.user.userprofile
    
    if not profile.is_verified:
        return redirect('verify_payment')
        
    return render(request, 'accounts/dashboard.html', {
        'profile': profile
    })


# --- ADD THIS: The Missing Payment Verification View ---
@login_required
def verify_payment(request):
    profile = request.user.userprofile
    
    # If they are already verified, don't make them do it again—send them to earn!
    if profile.is_verified:
        return redirect('dashboard')
        
    if request.method == 'POST':
        # This is where your form processing or payment check logic will run later.
        # For now, we will render the template page for them to see.
        pass

    return render(request, 'accounts/verify_payment.html', {
        'profile': profile
    })