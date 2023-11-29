# serializers.py
from rest_framework import serializers
from .models import Traveler, Trip, Feedback, Driver

class TravelerSerializer(serializers.ModelSerializer):
    feedback = serializers.SerializerMethodField()
    class Meta:
        model = Traveler
        fields = '__all__'
    
    def get_feedback(self, obj):
        feedback_objects = Feedback.objects.filter(traveler=obj)
        return FeedbackSerializer(feedback_objects, many=True).data

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    feedback = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ('trip_id', 'driver_name', 'feedback')

    def get_feedback(self, obj):
        feedback_objects = Feedback.objects.filter(trip=obj)
        return FeedbackSerializer(feedback_objects, many=True).data


class DriverSerializer(serializers.ModelSerializer):
    trips = TripSerializer(many=True, read_only=True)
    feedback = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = '__all__'

    def get_feedback(self, obj):
        trips = obj.trips.all()
        feedback_list = Feedback.objects.filter(trip__in=trips)
        return FeedbackSerializer(feedback_list, many=True).data