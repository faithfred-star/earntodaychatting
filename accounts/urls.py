from django.urls import path
from django.contrib.auth import views as auth_views  # Access built-in authentication forms
from . import views

urlpatterns = [
    # Main Landing Page Layout
    path('', views.home, name='home'),
    
    # Registration Route (Fixed: Mapped directly to the registration handler)
    path('register/', views.register, name='register'),
    
    # Authentication Management (Uses standard Django Class-Based Views)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Account Verification (Launches automated Pochi 0142512398 STK Push menu)
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    
    # Safaricom Daraja Webhook Endpoint (Listens for payment success data updates)
    path('verify-payment/mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
    
    # Verified Earning Area
    path('earning/', views.dashboard, name='dashboard'), 
]