from django.contrib import admin

from telegrambot.models import TgUser


# Register your models here.
@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'user')
    readonly_fields = ('chat_id', 'verification_code')
