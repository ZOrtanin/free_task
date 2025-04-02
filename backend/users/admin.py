from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User


class CustomUserAdmin(UserAdmin):
    print(333)
    print(UserAdmin.fields)

    fieldsets = (
        ('Информация', {'fields': ('last_name', 'first_name', 'middle_name')}),
        ('Учётная запись', {'fields': ('username', 'avatar')}),
        ('Безопасность', {'fields': ('password', 'phone_number', 'email')}),
        
        ('Дополнительно', {'fields': ('telegram_username',)}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'middle_name', 'first_name', 'last_name', 'email', 'password1', 'password2'),
            }),
        )

    # настройка общего списка пользователей
    list_display = ('avatar_preview', 'username', 'email', 'last_login')

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%"/>', obj.avatar.url)
        return "Нет фото"

    avatar_preview.short_description = "Аватар"

    # def my_username(self, obj):
    #     return obj.username
    # my_username.short_description = 'Пользователь'
    

# Register your models here.
admin.site.register(User, CustomUserAdmin)
