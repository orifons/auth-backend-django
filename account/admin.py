from django.contrib import admin

from account.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'date_joined',
        'is_active',
        'is_staff',
        'avatar'
    )
