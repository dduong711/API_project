# Generated by Django 3.0.11 on 2020-11-22 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mongodb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='host',
            new_name='host_name',
        ),
        migrations.RemoveField(
            model_name='host',
            name='db',
        ),
        migrations.AddField(
            model_name='host',
            name='db',
            field=models.ManyToManyField(related_name='host', to='mongodb.MongoDB'),
        ),
    ]