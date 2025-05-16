from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from django.shortcuts import redirect

from rest_framework import permissions
from rest_framework import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from crm.views import health_check
from contact.views import DynamicFormFieldViewSet, ContactViewSet
from appointment.views import AppointmentViewSet
from lists.views import ListViewSet

swagger_info = openapi.Info(
    title="CRM Service API",
    default_version='latest',
    description="A Buildly RAD Core Compatible Logic Module/microservice.",
)

schema_view = get_schema_view(
    swagger_info, public=True, permission_classes=(permissions.AllowAny,)
)

router = routers.SimpleRouter()

# Register your viewsets here
router.register(r'dynamic-form-field', DynamicFormFieldViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'appointment', AppointmentViewSet)
router.register(r'lists', ListViewSet)

urlpatterns = [
    re_path(r'^docs/swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('', health_check, name='custom_health_check'),
    path('health_check/', include('health_check.urls')),
    path('admin/', admin.site.urls),

]

urlpatterns += router.urls

urlpatterns += staticfiles_urlpatterns()
