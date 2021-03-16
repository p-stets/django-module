from django.contrib import admin
from django.db import models
from .models import User, Product, ProductIncome, ProductReturn
# Register your models here.

# admin.site.register((User, ProductIncome, ProductReturn, ))


class ProductAdmin(admin.ModelAdmin):
    model = Product
    fields = ('name', 'price', 'image', )
    readonly_fields = ('absolute_path', 'created_date', 'updated_date', )


admin.site.register((Product, ))
