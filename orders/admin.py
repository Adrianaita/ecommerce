from django.contrib import admin

from store.models import Order, OrderItem, ShippingAddress

class OrderItemInlineAdmin(admin.TabularInline):
    model = OrderItem
    min_num = 1
    extra = 0
    readonly_fields = ('product', 'quantity', 'get_subtotal')

    def get_subtotal(self, obj):
        return obj.get_total
    get_subtotal.short_description = 'Subtotal'

class ShippingAddressInlineAdmin(admin.StackedInline):
    model = ShippingAddress
    extra = 0
    readonly_fields = ('address', 'city', 'state', 'zipcode')

@admin.register(Order)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'date_ordered', 'is_complete', 'transaction_id')
    list_filter = ('complete', 'date_ordered')
    search_fields = ('customer__email', 'transaction_id')
    inlines = [OrderItemInlineAdmin, ShippingAddressInlineAdmin]
    ordering = ('-date_ordered',)

    def customer_name(self, obj):
        return obj.customer.name if obj.customer else 'Anonimo'
    customer_name.short_description = 'Cliente'

    def is_complete(self, obj):
        return obj.complete
    is_complete.boolean = True
    is_complete.short_description = 'Completo'

