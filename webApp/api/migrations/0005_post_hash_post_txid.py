# Generated by Django 4.0.1 on 2022-02-19 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_useripaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hash',
            field=models.CharField(default=None, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='txId',
            field=models.CharField(default=None, max_length=66, null=True),
        ),
    ]