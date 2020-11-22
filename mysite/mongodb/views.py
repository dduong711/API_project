from datetime import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from .serializers import MongoDBSerializer
from .models import MongoDB
from .tasks import notify


class MongoDBViewSet(viewsets.ModelViewSet):
    serializer_class = MongoDBSerializer
    queryset = MongoDB.objects.all()
    renderder_classes = [BrowsableAPIRenderer, ]
    permission_classes = [AllowAny, ]

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        # notify admin
        context = {
            "user": str(self.request.user),
            "method": self.request.method,
            "data": self.request.data,
            "url": self.request.build_absolute_uri(),
            "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        notify.delay(context)

        return response

    def create(self, request):
        data = {
            "hosts": request.data["host"],
            "db_user": request.data["db_user"],
            "db_password": request.data["db_password"],
            "db_name": request.data["db_name"],
        }
        conn_str = MongoDB.generate_connection_string(**data)
        try:
            client = MongoClient(conn_str, serverSelectionTimeoutMS=3000)
            _ = client.server_info()
        except ServerSelectionTimeoutError as Err:
            return Response({"error": Err}, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "Error 400: Bad Request!"})
        return super().create(request)