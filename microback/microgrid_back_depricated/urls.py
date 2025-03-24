from django.urls import path
from . import views



urlpatterns = [
    # Define your app-specific URLs here
    # For example:
    # path('measurements/', views.MeasurementListView.as_view(), name='measurement-list'),
    # path('measurements/<int:pk>/', views.MeasurementDetailView.as_view(), name='measurement-detail'),
    
    path('measurements/<int:table_no>/<int:sensor_id>/', views.measurements_by_sensor_id, name='measurements_by_sensor_id'),
]