from django.urls import path
from . import views

urlpatterns = [
    path('events-list/', views.events, name='events-list'),
    path('create-event/', views.createEvent, name='create-event'),
    path('create-event/<str:worker_id>/<str:when>/', views.createEvent, name='create-event'),
    path('update-event/<str:pk>/', views.updateEvent, name='update-event'),
    path('update-event/<str:pk>/', views.updateEvent, name='update-event'),
    path('delete-event/<str:pk>/', views.deleteEvent, name='delete-event'),
    path('events-approval/', views.eventsApproval, name='events-approval'),

    path('calendar/<str:specialist_id>/<int:year>/<str:month>/', views.timetable, name='calendar'),
    path('calendar/<str:specialist_id>/<int:year>/<str:month>/<int:day>', views.calendarDay, name='day'),
]