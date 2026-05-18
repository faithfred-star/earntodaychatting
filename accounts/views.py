from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def verify_payment(request):
    profile = request.user.userprofile
    
    # If they are already verified, don't show this page
    if profile.is_verified:
        return redirect('dashboard')  # Redirect to your app's dashboard/home

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        # Save the phone number they used to pay
        profile.phone_number = phone_number
        profile.save()
        
        # Redirect to a waiting page or show a success message
        return render(request, 'accounts/verification_pending.html', {
            'phone_number': phone_number
        })

    return render(request, 'accounts/verify_payment.html')