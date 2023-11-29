from django.db import models
from django.contrib.auth.models import User

class Traveler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional traveler-related fields if needed
    def __str__(self):
        return self.user.username

class Driver(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=20)
    # Add other driver-related fields as needed

    def __str__(self):
        return self.name.username


class Trip(models.Model):
    trip_id = models.CharField(max_length=20, unique=True)
    driver_name = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips')
    # Add other trip-related fields as needed
    def __str__(self):
        return f"{self.trip_id} ({self.driver_name})"
    
    def get_feedback(self):
        return Feedback.objects.filter(trip=self.trip_id)
         

class Feedback(models.Model):
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE,related_name='feedback_set')
    question1 = models.TextField()  # Customizable question
    question2 = models.TextField()  # Customizable question
    comments = models.TextField(blank=True, null=True)
    # Add other feedback-related fields as needed
    def __str__(self):
        return f"{self.traveler.user.username} - {self.trip.trip_id}"