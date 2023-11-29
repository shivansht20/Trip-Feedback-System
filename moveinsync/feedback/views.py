# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Traveler, Trip, Feedback
from .serializers import TravelerSerializer, TripSerializer, FeedbackSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Trip, Feedback, Driver
from .serializers import TripSerializer, FeedbackSerializer, DriverSerializer
from rest_framework.views import APIView
from rest_framework import status


class TravelerDetailView(generics.RetrieveAPIView):
    queryset = Traveler.objects.all()
    serializer_class = TravelerSerializer
    permission_classes = [IsAuthenticated]

# class TripDetailView(generics.RetrieveAPIView):
#     queryset = Trip.objects.all()
#     serializer_class = TripSerializer
#     # permission_classes = [IsAuthenticated]

class TravelerFeedbackView(generics.RetrieveAPIView):
    queryset = Traveler.objects.all()
    serializer_class = TravelerSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        feedback_data = serializer.data.get('feedback')
        return Response(feedback_data)

class TripDetailView(APIView):
    def get(self, request, pk):
        try:
            trip = Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            return Response({"error": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TripSerializer(trip)
        feedback_serializer = FeedbackSerializer(trip.feedback_set.all(), many=True)

        response_data = serializer.data
        response_data['feedback'] = feedback_serializer.data

        return Response(response_data)

class FeedbackListView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = []

class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

class DriverFeedbackAPIView(APIView):
    def get(self, request, driver_id):
        try:
            driver = Driver.objects.get(pk=driver_id)
        except Driver.DoesNotExist:
            return Response({"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DriverSerializer(driver)
        return Response(serializer.data)