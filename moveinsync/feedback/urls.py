# urls.py
from django.urls import path
from .views import TravelerDetailView, TripDetailView, FeedbackListView, FeedbackDetailView, TravelerFeedbackView, DriverFeedbackAPIView

urlpatterns = [
    path('traveler/<int:pk>/', TravelerDetailView.as_view(), name='traveler-detail'),
    path('trip/<int:pk>/', TripDetailView.as_view(), name='trip-detail'),
    path('feedback/', FeedbackListView.as_view(), name='feedback-list'),
    path('feedback/<int:pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),
    path('travelers/<int:pk>/feedback/', TravelerFeedbackView.as_view(), name='traveler-feedback'),
    path('drivers/<int:driver_id>/', DriverFeedbackAPIView.as_view(), name='driver-feedback'),

]
