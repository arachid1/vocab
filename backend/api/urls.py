from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WordViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r"words", WordViewSet)
router.register(r"profiles", UserProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
