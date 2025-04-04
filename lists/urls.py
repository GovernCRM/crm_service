from rest_framework import routers

from .views import ListViewSet

# add urls
router = routers.SimpleRouter()

router.register(r'lists', ListViewSet)

urlpatterns = router.urls
