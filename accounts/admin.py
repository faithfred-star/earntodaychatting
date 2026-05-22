from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Added fields to display tracking on your Django Admin panel list view
    list_display = ('user', 'phone_number', 'is_verified', 'referral_code', 'mpesa_checkout_id')
    list_filter = ('is_verified',)
    search_fields = ('user__username', 'phone_number', 'referral_code', 'mpesa_checkout_id')