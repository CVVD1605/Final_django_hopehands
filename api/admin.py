from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Volunteer

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    # Customize the admin interface
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    model = Volunteer
    list_display = ('get_first_name', 'get_last_name', 'get_email', 'phone', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

    # ✅ Fix: Correctly reference the `User` fields via `user`
    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else "N/A"
    get_first_name.admin_order_field = 'user__first_name'  # Enables sorting
    get_first_name.short_description = 'First Name'  # Sets column header

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else "N/A"
    get_last_name.admin_order_field = 'user__last_name'
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email if obj.user else "N/A"
    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'
