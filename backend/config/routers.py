from rest_framework.routers import DefaultRouter

from linkanywhere.apps.categories.views import CategoryViewSet
from linkanywhere.apps.links.views import LinkViewSet
from linkanywhere.apps.tags.views import TagViewSet
from linkanywhere.apps.users.views import UserViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'links', LinkViewSet)
router.register(r'tags', TagViewSet)
router.register(r'users', UserViewSet)
