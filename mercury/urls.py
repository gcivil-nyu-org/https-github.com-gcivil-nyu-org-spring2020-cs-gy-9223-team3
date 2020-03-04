from django.urls import path, include, re_path
from .views import simulator, views, dashboard, can, stopwatch, hardware
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "mercury"

schema_view = get_schema_view(
    openapi.Info(
        title="Mercury API for Motorsports Telemetry",
        default_version="v1",
        description="Mercury API is a simple API \
            allowing onboard computer and pit crew to log and monitor system performance.",
        terms_of_service="tbd",
        contact=openapi.Contact(email="mercury@example.com"),
        license=openapi.License(name="tbd"),  
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", views.EventAccess.as_view(), name="EventAccess"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("index", views.HomePageView.as_view(), name="index"),
    path("simulator/", simulator.SimulatorView.as_view(), name="simulator"),
    path("dashboard/", dashboard.DashboardView.as_view(), name="dashboard"),
    path("stopwatch/", stopwatch.StopwatchView.as_view(), name="stopwatch"),
    path("api/can/", can.post, name="can-api"),  # CAN API Ingestion endpoint
    path("can/", can.CANUI.as_view(), name="can-ui"),  # CAN Decoder UI endpoint
    path("hardware", hardware.HardwareView.as_view(), name="hardware"),  # Hardware API
    path("api/v1/", include("api.urls"), name="api"),
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
