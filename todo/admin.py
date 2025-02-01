from django.contrib import admin
from django.utils.html import format_html
from .models import UserName, Item

class ItemInline(admin.TabularInline):  # Inline representation for related Items
    model = Item
    extra = 1  

class UsersAdmin(admin.ModelAdmin):
    list_display = ("username", "get_items")  
    inlines = [ItemInline]  # Embed ItemInline in UserName admin page
    
    def get_items(self, obj):
        return ", ".join([item.item_text for item in obj.item.all()])

    get_items.short_description = "Items"

class ItemAdmin(admin.ModelAdmin):
    list_display = ("username", "item_text", "is_done", "pub_date") 

admin.site.register(UserName, UsersAdmin)
admin.site.register(Item, ItemAdmin)
