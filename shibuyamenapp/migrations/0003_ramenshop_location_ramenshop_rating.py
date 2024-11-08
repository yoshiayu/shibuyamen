# Generated by Django 4.2.16 on 2024-10-26 01:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("shibuyamenapp", "0002_ramenshop_link_alter_ramenshop_opening_hours"),
    ]

    operations = [
        migrations.AddField(
            model_name="ramenshop",
            name="location",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ramenshop",
            name="rating",
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
            preserve_default=False,
        ),
    ]
