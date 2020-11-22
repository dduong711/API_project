from django.db import models


class MongoDB(models.Model):
    db_user = models.CharField(max_length=256)
    db_password = models.CharField(max_length=256)
    db_name = models.CharField(max_length=512)

    @staticmethod
    def generate_connection_string(hosts=None, db_user=None, db_password=None, db_name=None):
        if not all([hosts, db_user, db_password, db_name]):
            raise Exception("Cannot generate connection string!")
        if len(hosts) == 1:
            host_name = hosts[-1]["host_name"]
        else:
            host = [f"{host['host_name']}:{host['port']}" for host in hosts]
            host_name = ",".join(host)
        return f"mongodb+srv://{db_user}:{db_password}@{host_name}/{db_name}"

    def __str__(self):
        return str(self.id)


class Host(models.Model):
    host_name = models.CharField(max_length=128, default="0.0.0.0")
    port = models.IntegerField(null=True, blank=True)
    db = models.ManyToManyField(MongoDB, related_name="host")

    def __str__(self):
        print(self.db.all())
        dbs = ", ".join([str(db.id) for db in self.db.all()])
        if self.port:
            return f"{self.host_name}:{self.port} ({dbs})"
        return f"{self.host_name} ({dbs})"