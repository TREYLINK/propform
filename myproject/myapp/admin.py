from django.contrib import admin
from .models import Developer, Building, Apartment, Buyer, Order, Land, Land_m, UserProfile, Event

admin.site.register(Developer)
admin.site.register(Building)
admin.site.register(Apartment)
admin.site.register(Order)
admin.site.register(Buyer)
admin.site.register(Land)
admin.site.register(UserProfile)
admin.site.register(Land_m)
admin.site.register(Event)