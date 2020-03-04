from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

app_name = "api"
urlpatterns = [
    path("events/", views.EventList.as_view(), name="event-list"),
    path("events/<uuid:pk>/", views.EventDetail.as_view(), name="event-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
