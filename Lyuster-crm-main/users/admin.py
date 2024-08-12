from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import ClientUser, User, UserProfile
from django.utils.html import format_html



@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_filter = ('created_at',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return None

    image_tag.short_description = 'Image'
    list_display = ('first_name', 'last_name', 'phone_number', 'created_at', 'image_tag')



class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'
    fields = ('date_joined', 'status', 'country', 'languages_known', 'telegram', 'location')
    extra = 0

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    
    # Remove 'date_joined' from fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login',)}),  # Removed 'date_joined'
    )
    
    # No change needed in add_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number', 'is_active', 'is_staff')
        }),
    )
    
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    inlines = [UserProfileInline]

admin.site.register(User, UserAdmin)
