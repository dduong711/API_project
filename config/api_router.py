from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from mysite.users.api.views import UserViewSet
from mysite.mongodb.views import MongoDBViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("mongodb", MongoDBViewSet)


app_name = "api"
urlpatterns = router.urls
