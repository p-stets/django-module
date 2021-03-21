from django.contrib import admin
from .models import User, Product, ProductIncome, ProductSell
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('id', 'password', 'email', 'username', 'first_name', 'last_name',
              'is_staff', 'is_active', 'date_joined', 'base_wallet', 'current_money', )
    readonly_fields = ('id', 'current_money', )
    list_display = ('email', 'username', 'base_wallet', 'current_money')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    fields = ('id', 'name', 'price', 'current_stock', 'image', 'image_path', 'create_date', 'update_date', )
    readonly_fields = ('id', 'current_stock', 'image_path', 'create_date', 'update_date', )
    list_display = ('id', 'name', 'price', 'current_stock', 'create_date', 'update_date', )


@admin.register(ProductIncome)
class ProductIncomeAdmin(admin.ModelAdmin):
    model = ProductIncome
    fields = ('id', 'product', 'quantity', 'user', 'status', 'create_date', 'update_date', )
    readonly_fields = ('id', 'create_date', 'update_date', )
    list_display = ('id', 'product', 'quantity', 'user', 'create_date', )


@admin.register(ProductSell)
class ProductReturnAdmin(admin.ModelAdmin):
    model = ProductSell
    fields = ('id', 'product', 'quantity', 'user', 'status', 'create_date', 'update_date', )
    readonly_fields = ('id', 'create_date', 'update_date', )
    list_display = ('id', 'product', 'quantity', 'user', 'create_date', )
