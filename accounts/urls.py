from django.urls import path
from . import views  # This is completely safe here!

urlpatterns = [
    # This empty string rule handles your main home landing page safely!
    path('', views.home, name='home'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
    path('earning/', views.dashboard, name='dashboard'), 
]