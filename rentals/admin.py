from django.contrib import admin
from .models import Snowboard, Renter, Rental

class RentalAdmin(admin.ModelAdmin):
    list_display = ('renter', 'snowboard', 'rental_date', 'return_date', 'is_active')
    list_filter = ('renter', 'snowboard', 'rental_date', 'return_date')
    search_fields = ('renter__username', 'snowboard__name')

def is_active(self, obj):
    return obj.return_date is None
is_active.boolean = True
is_active.short_description = 'Active Rental'

admin.site.register(Renter)
admin.site.register(Rental, RentalAdmin)
admin.site.register(Snowboard)
