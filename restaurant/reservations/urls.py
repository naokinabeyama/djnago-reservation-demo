from django.urls import path
from . import views
from .views import (
    ReservationDeleteView, ReservationsListView, ReservationDetailView
)

app_name = 'reservations'

urlpatterns = [
    path('reservation', views.ReservationView, name='reservation'),
    path('reservationsList', ReservationsListView.as_view(), name='reservationsList'),
    path('reservationDetail/<int:pk>', ReservationDetailView.as_view(), name='reservationDetail'),
    path('reservationUpdate/<int:pk>', views.ReservationUpdateView, name='reservationUpdate'),
    path('reservationDelete/<int:pk>', ReservationDeleteView.as_view(), name='reservationDelete'),

    
]
