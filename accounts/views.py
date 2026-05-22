from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import json
import logging

logger = logging.getLogger(__name__)

# --- M-PESA AUTOMATION CONFIGURATION ---
MPESA_CONSUMER_KEY = "YOUR_LIVE_CONSUMER_KEY"
MPESA_CONSUMER_SECRET = "YOUR_LIVE_CONSUMER_SECRET"
MPESA_PASSKEY = "YOUR_LIVE_LIPA_NA_MPESA_PASSKEY"

# Your official Pochi la Biashara number formatted for production APIs
POCHI_SHORTCODE = "254142512398" 
# Change this line in views.py
CALLBACK_URL = "https://earntodaychatting.onrender.com/verify-payment/mpesa-callback/"
def get_mpesa_access_token():
    api_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    try:
        response = requests.get(api_url, auth=HTTPBasicAuth(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET))
        if response.status_code == 200:
            return response.json().get('access_token')
    except Exception as e:
        logger.error(f"Failed generating M-Pesa token: {e}")
    return None

def initiate_stk_push(phone_number, amount, account_reference):
    access_token = get_mpesa_access_token()
    if not access_token:
        return False, "Access token generation failed"

    # Standardize target handset phone formatting
    if phone_number.startswith('0'):
        phone_number = '254' + phone_number[1:]
    elif phone_number.startswith('+254'):
        phone_number = phone_number[1:]
        
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = POCHI_SHORTCODE + MPESA_PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode('utf-8')
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "BusinessShortCode": POCHI_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",  # Pochi targets route through Paybill type architecture
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": POCHI_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": "Earning Account Activation"
    }
    
    api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        return True, response.json()
    except Exception as e:
        return False, str(e)


# --- APPLICATION VIEWS ---

def home(request):
    if request.user.is_authenticated:
        if not request.user.userprofile.is_verified:
            return redirect('verify_payment')
        return redirect('dashboard')
    return render(request, 'accounts/home.html')

def register(request):
    ref_code = request.GET.get('ref', '')
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'accounts/register.html', {'ref_code': ref_code})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'accounts/register.html', {'ref_code': ref_code})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.save()

        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            referral_code=ref_code,
            is_verified=False
        )

        login(request, user)
        return redirect('verify_payment')

    return render(request, 'accounts/register.html', {'ref_code': ref_code})

@login_required
def dashboard(request):
    profile = request.user.userprofile
    if not profile.is_verified:
        return redirect('verify_payment')
    return render(request, 'accounts/dashboard.html', {'profile': profile})

@login_required
def verify_payment(request):
    profile = request.user.userprofile
    if profile.is_verified:
        return redirect('dashboard')
        
    if request.method == 'POST':
        submitted_phone = request.POST.get('phone_number')
        profile.phone_number = submitted_phone
        profile.save()
        
        # Fire automated push
        success, response_data = initiate_stk_push(
            phone_number=submitted_phone,
            amount=119,
            account_reference=profile.user.username
        )
        
        if success and response_data.get("ResponseCode") == "0":
            profile.mpesa_checkout_id = response_data.get("CheckoutRequestID")
            profile.save()
            return render(request, 'accounts/verification_pending.html', {'phone_number': submitted_phone})
        else:
            err = response_data.get("ResponseDescription", "STK initiation error.") if isinstance(response_data, dict) else response_data
            messages.error(request, f"Failed: {err}. Double check your entry format.")
            return redirect('verify_payment')

    return render(request, 'accounts/verify_payment.html', {'profile': profile})

# Instant automated Safaricom callback URL
@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            callback_data = json.loads(request.body)
            stk_callback = callback_data['Body']['stkCallback']
            result_code = stk_callback['ResultCode']
            checkout_id = stk_callback['CheckoutRequestID']
            
            if result_code == 0:
                try:
                    profile = UserProfile.objects.get(mpesa_checkout_id=checkout_id)
                    profile.is_verified = True
                    profile.save()
                except UserProfile.DoesNotExist:
                    logger.warning(f"Unknown checkout request received: {checkout_id}")
                    
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})
        except Exception as e:
            logger.error(f"Callback structure exception: {e}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Processing failure"}, status=400)
            
    return JsonResponse({"Error": "Method Not Allowed"}, status=405)