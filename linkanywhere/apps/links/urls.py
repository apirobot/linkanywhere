from rest_framework.routers import DefaultRouter

from .views import LinkViewSet, TagViewSet

router = DefaultRouter()
router.register(r'links', LinkViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = router.urls
