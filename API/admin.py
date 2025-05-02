from django.contrib import admin
from .models import (
    Supplier, InvestmentPerformance, Investment, MonthlySalesStock, Product,
    Stock, Customer, Order, Sale, StockHistory, RestockRequest, MonthlyInvestment, StockInvestment
)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email')
    search_fields = ('name', 'email')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'sku', 'unit_price', 'supplier')
    search_fields = ('name', 'sku')
    list_filter = ('category',)

class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    search_fields = ('product__name',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_date', 'total_amount')
    search_fields = ('customer__name',)
    list_filter = ('order_date',)

class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity_sold', 'sale_price', 'sale_date', 'status')
    search_fields = ('product__name', 'customer__name')
    list_filter = ('sale_date', 'status')

class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ('transaction_date', 'transaction_type', 'product', 'stock_change', 'starting_stock', 'total_revenue')
    search_fields = ('product__name', 'sku')
    list_filter = ('transaction_type',)

class RestockRequestAdmin(admin.ModelAdmin):
    list_display = ('product', 'requested_quantity', 'request_date', 'status')
    search_fields = ('product__name',)
    list_filter = ('status',)

@admin.register(MonthlySalesStock)
class MonthlySalesStockAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'sales', 'stock')
    list_filter = ('year',)

# Add ModelAdmin for Investment
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'supplier', 'amount', 'date_invested')
    search_fields = ('user__username', 'supplier__name')

# Add ModelAdmin for InvestmentPerformance
class InvestmentPerformanceAdmin(admin.ModelAdmin):
    list_display = ('investment', 'current_value', 'growth_rate')
    search_fields = ('investment__user__username',)

@admin.register(MonthlyInvestment)
class MonthlyInvestmentAdmin(admin.ModelAdmin):
    list_display = ('investment', 'month', 'value')
    search_fields = ('investment__user__username',)
    list_filter = ('month',)

# Add ModelAdmin for StockInvestment
class StockInvestmentAdmin(admin.ModelAdmin):
    list_display = ('investment', 'stock', 'date_linked')  # Fields to display in the admin list view
    search_fields = ('investment__user__username', 'stock__product__name')  # Fields to search by
    list_filter = ('date_linked',)  # Filters for the admin list view

# Register models with their respective ModelAdmin classes
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(StockHistory, StockHistoryAdmin)
admin.site.register(RestockRequest, RestockRequestAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(InvestmentPerformance, InvestmentPerformanceAdmin)
admin.site.register(StockInvestment, StockInvestmentAdmin)  # Register StockInvestment