from django.contrib import admin
from .models import Goods, Category
from django.utils.safestring import mark_safe
# Register your models here.

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name','photo', 'time_create', 'status', 'card_photo') 
    list_display_links = ('name',)
    readonly_fields = ('slug',)
    ordering = ['time_create', 'name']
    list_editable = ("status",)
    actions = ['set_status']
    search_fields = ['name']
    list_filter = ['status']
    save_on_top = True


    @admin.display(description='Фото', ordering='desc')
    def card_photo(self, goods:Goods):
        if goods.photo:
          return mark_safe(f"<img src='{goods.photo.url}' width=50>")
        return 'Без фото'
        
    @admin.action(description='Опубликовать')
    def set_status(self, request, queryset):
        count = queryset.update(status=Goods.Status.IN_STOCK)
        self.message_user(request, f"Изменено {count} записей")

@admin.register(Category)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


# admin.site.register(Goods, WomenAdmin)