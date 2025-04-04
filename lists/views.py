from rest_framework import viewsets, permissions

from lists.models import List
from lists.serializers import ListSerializer


class ListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lists to be viewed or edited.
    """
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'list_uuid'

    def perform_create(self, serializer):
        serializer.save()
