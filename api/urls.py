from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import WorkerViewSet, ClientViewSet, EventViewSet


router = SimpleRouter()
router.register('workers', WorkerViewSet, basename='workers')
router.register('clients', ClientViewSet, basename='clients')
router.register('events', EventViewSet, basename='events-api')

urlpatterns = router.urls
