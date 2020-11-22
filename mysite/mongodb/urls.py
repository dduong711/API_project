# urls.py

from rest_framework import routers

from .views import MongoDBViewset


router = routers.SimpleRouter()

router.register(r'mongodb', MongoDBViewset)

urlpatterns = router.urls
