from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from lists.filters import ListFilter
from lists.models import List
from lists.serializers import CommunitySerializer, ListSerializer, ListSlimSerializer


class ListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lists to be viewed or edited.
    """

    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ListFilter
    lookup_field = "list_uuid"

    def list(self, request, *args, **kwargs):
        """
        Override the list method to include custom logic if needed.
        """
        queryset = super(ListViewSet, self).get_queryset()

        # check if nested list is requested
        if "nested" in request.query_params:
            queryset = queryset.filter(parent__isnull=True).prefetch_related(
                "sub_lists__sub_lists"
            )
            # Paginate manually
            paginator = self.pagination_class()
            paginated_qs = paginator.paginate_queryset(queryset, request, view=self)

            serializer = CommunitySerializer(paginated_qs, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Default behavior for non-nested lists
        return super(ListViewSet, self).list(request, *args, **kwargs)

    @action(detail=True, methods=["get"], url_path="sub-list", url_name="sub_list")
    def sub_list(self, request, list_uuid=None):
        """
        Custom action to get children of a list.
        """
        try:
            instance = self.get_object()
            children = instance.sub_lists.all()
            serializer = ListSerializer(children, many=True)
            return Response(serializer.data)
        except List.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        """
        Override the get_serializer_class method to return different serializers based on the action.
        """
        if self.action == "list":
            return ListSlimSerializer
        return super(ListViewSet, self).get_serializer_class()
