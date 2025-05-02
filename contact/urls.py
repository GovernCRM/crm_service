from rest_framework import routers

from contact.views import ContactViewSet, DynamicFormFieldViewSet

# add urls
router = routers.SimpleRouter()

router.register(r'dynamic-form-field', DynamicFormFieldViewSet)
router.register(r'contact', ContactViewSet)

urlpatterns = router.urls
