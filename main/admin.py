from django.contrib import admin
from .models import Business, User, Customer, Order

admin.site.register(Business)
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Order)