# Generated by Django 3.2.13 on 2022-07-06 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_events_google_event_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='google_event_id',
        ),
    ]
