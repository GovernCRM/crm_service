from django.urls import re_path, include, path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from appointment import views as views_apppointment

router = routers.SimpleRouter()

router.register(r'appointment', views_apppointment.AppointmentViewSet)
router.register(r'appointmentnotifications',
                views_apppointment.AppointmentNotificationViewSet)

urlpatterns = [
    re_path(r'^docs/', include_docs_urls(title='CRM Service')),
    re_path(r'^api/', include('contact.urls')),
]

urlpatterns += router.urls
