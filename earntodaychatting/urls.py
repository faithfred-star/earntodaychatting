from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
    
    # --- This maps /earning/ to your dashboard/earning view ---
    path('earning/', views.dashboard, name='dashboard'), 
]