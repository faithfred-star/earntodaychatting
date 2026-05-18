from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages

def register_view(request):
    # Grab the referral code from the URL query string if present (e.g., ?ref=JQTY7RCQ)
    ref_code = request.GET.get('ref', 'GLOBAL_USER')
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        form_ref_code = request.POST.get('ref')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'register.html', {'ref_code': form_ref_code})

        # Split full name into first and last name safely
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        
        # Save profile tracking information
        UserProfile.objects.create(user=user, referral_code=form_ref_code)
        
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('register')

    return render(request, 'register.html', {'ref_code': ref_code})