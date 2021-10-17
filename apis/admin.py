from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register( City )
admin.site.register(Cinema)
admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(Ticket)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register( MovieCinemaShow )