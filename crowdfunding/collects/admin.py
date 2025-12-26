from django.contrib import admin
from collects.models import Collect, Payment


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'occasion', 'target_amount', 'collected_amount', 'end_date')
    search_fields = ('name', 'author__email')
    list_filter = ('occasion', 'end_date')
    readonly_fields = ('collected_amount', 'donors_count')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'collect', 'amount', 'date')
    search_fields = ('user__email', 'collect__name')
    list_filter = ('date',)
