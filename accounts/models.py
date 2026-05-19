from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Links each profile directly to a unique user account
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Stores the optional referral code (blank=True allows users to leave it empty)
    referral_code = models.CharField(max_length=50, blank=True, null=True)
    
    # Captures the mobile money phone number for payment tracking
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Tracks payment verification status for the 119 KSh activation fee
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Verified: {self.is_verified}"