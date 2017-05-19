from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, LinkViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'links', LinkViewSet)

urlpatterns = router.urls
