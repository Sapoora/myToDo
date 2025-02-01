from django.contrib import admin

from .models import UserName, Item


class UsersAdmin(admin.ModelAdmin):
    fields = ["username", "question_text"]


admin.site.register(UserName, UsersAdmin)
admin.site.register(Item)