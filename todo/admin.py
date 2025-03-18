from django.contrib import admin
from django.utils.html import format_html
from .models import User, Item

class ItemInline(admin.TabularInline):  # Inline representation for related Items
    model = Item
    extra = 1  

class UsersAdmin(admin.ModelAdmin):
    list_display = ("username", "get_items")  
    inlines = [ItemInline]  # Embed ItemInline in UserName admin page
    
    def get_items(self, obj):
        return ", ".join([item.item_text for item in obj.items.all()])

    get_items.short_description = "Items"

class ItemAdmin(admin.ModelAdmin):
    list_display = ("user", "item_text", "status", "pub_date") 

admin.site.register(User, UsersAdmin)
admin.site.register(Item, ItemAdmin)
