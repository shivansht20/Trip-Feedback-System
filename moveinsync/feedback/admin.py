# admin.py
from django.contrib import admin
from .models import Traveler, Trip, Feedback, Driver

@admin.register(Traveler)
class TravelerAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name','license_number')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('trip_id', 'driver_name',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('traveler', 'trip', 'question1', 'question2', 'comments',)
