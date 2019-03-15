from django.db import models
from django.contrib.postgres.fields import JSONField
from oauth2_provider.settings import oauth2_settings


class SoftwareStatement(models.Model):
    statement = JSONField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    application = models.ForeignKey(
        oauth2_settings.APPLICATION_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
