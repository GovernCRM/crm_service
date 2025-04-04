from django.contrib.postgres.fields.array import ArrayField
from django.db import models


class List(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="sub_lists")
    contacts = ArrayField(models.CharField(max_length=255), null=True, blank=True)
    user_uuid = models.UUIDField(blank=True, null=True)
    polygon = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
