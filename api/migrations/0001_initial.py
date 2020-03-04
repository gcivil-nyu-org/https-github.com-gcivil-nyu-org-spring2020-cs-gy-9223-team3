from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AGEvent",
            fields=[
                (
                    "event_uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("event_name", models.CharField(blank=True, max_length=40)),
                ("event_date", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "event_description",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
        )
    ]
