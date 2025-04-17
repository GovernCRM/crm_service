import uuid

from django.contrib.postgres.fields.array import ArrayField
from django.db import models

class ListTypes(models.TextChoices):
    COMMUNITY = "community", "Community"
    LIST = "list", "List"
    GROUP = "group", "Group"


class List(models.Model):
    list_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    organization_uuid = models.UUIDField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="sub_lists")
    contacts = ArrayField(models.CharField(max_length=255), null=True, blank=True)
    contact_objects = models.JSONField(blank=True, null=True)
    list_type = models.CharField(max_length=20, choices=ListTypes.choices, default=ListTypes.LIST)
    user_uuid = models.UUIDField(blank=True, null=True)
    polygon = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    open_polls = models.IntegerField(default=0, blank=True, null=True)
    pending_engagements = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name