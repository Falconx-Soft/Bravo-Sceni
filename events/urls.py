from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.get_events, name="events"),
    path('view_event/<int:id>', views.view_event, name="view_event"),
    path('add_events/', views.add_events, name="add_events"),
    path('delete_events/<int:id>', views.delete_events, name="delete_events"),
    path('edit_events/<int:id>', views.edit_events, name="edit_events"),

    path('search/', views.search, name="search"),

    path('calendar/', views.calendar, name="calendar"),
]