# Generated by Django 3.1.4 on 2021-03-06 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contractApp', '0008_delete_client'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contracts',
            new_name='Contract',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
