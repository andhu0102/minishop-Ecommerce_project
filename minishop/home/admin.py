from django.contrib import admin
from . models import *
# Register your models here.

class cateadmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(cate, cateadmin)


class productadmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'img', 'available']
    list_editable = ['price', 'stock', 'img', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(product, productadmin)