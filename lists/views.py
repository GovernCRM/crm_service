from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from lists.models import List
from lists.serializers import ListSerializer, CommunitySerializer


class ListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lists to be viewed or edited.
    """
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['list_type', 'organization_uuid']
    lookup_field = 'list_uuid'

    def list(self, request, *args, **kwargs):
        """
        Override the list method to include custom logic if needed.
        """
        queryset = super(ListViewSet, self).get_queryset()

        # check if nested list is requested
        if 'nested' in request.query_params:
            queryset = queryset.filter(parent__isnull=True).prefetch_related('sub_lists__sub_lists')
            serializer = CommunitySerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Default behavior for non-nested lists
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()
