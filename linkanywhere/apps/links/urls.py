from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, LinkViewSet, TagViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'links', LinkViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = router.urls
