# serializers.py

from rest_framework import serializers

from .models import MongoDB, Host


class HostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Host
        fields = ["host_name", "port"]


class MongoDBSerializer(serializers.ModelSerializer):
    # host = serializers.StringRelatedField(many=True)
    host = HostSerializer(many=True)

    class Meta:
        model = MongoDB
        fields = ["id", "host", "db_user", "db_password", "db_name"]

    def create(self, validated_data):
        hosts_data = validated_data.pop("host")
        mgdb = MongoDB.objects.create(**validated_data)
        for host_data in hosts_data:
            host_name = host_data["host_name"]
            port = host_data["port"]
            host = Host.objects.create(host_name=host_name, port=port)
            mgdb.host.add(host)
        return mgdb

    def update(self, mgdb, validated_data):
        host_data = validated_data.pop("host")

        # remove
        for mgdb_host in mgdb.host.all():
            remove = True
            for host in host_data:
                if mgdb_host.host_name == host["host_name"] and mgdb_host.port == host["port"]:
                    remove = False
                    break
            if remove:
                mgdb.host.remove(mgdb_host)
    
        # add
        for host in host_data:
            host_name = host["host_name"]
            port = host["port"]
            try:
                mgdb_host = mgdb.host.get(host_name=host_name, port=port)
            except Host.DoesNotExist:
                new_host = Host.objects.create(host_name=host_name, port=port)
                mgdb.host.add(new_host)

        mgdb.db_user = validated_data.get("db_user", mgdb.db_user)
        mgdb.db_password = validated_data.get("db_password", mgdb.db_password)
        mgdb.db_name = validated_data.get("db_name", mgdb.db_name)
        mgdb.save()

        return mgdb
