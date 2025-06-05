from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_artist', 'is_approved')
    list_filter = ('is_artist', 'is_approved')
    search_fields = ('username', 'email')

    # Add actions for bulk approval
    actions = ['approve_artists']

    def approve_artists(self, request, queryset):
        queryset.update(is_approved=True)
    approve_artists.short_description = "Approve selected artists"
