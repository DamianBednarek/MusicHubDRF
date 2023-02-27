from uuid import uuid4

from django.db import models


class Meta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
