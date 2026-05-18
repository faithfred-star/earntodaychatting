from django.urls import path
# --- FIXED: Added the missing views import ---
from django.urls import path, include
urlpatterns = [
    # Main landing page
    path('', views.home, name='home'),
    
    # Matches your existing setup exactly (using a hyphen)
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    
    # Maps /earning/ to your dashboard view
    path('earning/', views.dashboard, name='dashboard'), 
]