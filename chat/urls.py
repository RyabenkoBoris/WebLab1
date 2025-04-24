from django.urls import path, include
from .views import AppInfoView

from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MessageViewSet

router = DefaultRouter()
router.register('', ChatViewSet, basename='chat')
router.register(r'message', MessageViewSet, basename='message')

urlpatterns = router.urls

urlpatterns = [
    path("about/", AppInfoView.as_view(), name="about"),
    path('', include(router.urls)),
]
