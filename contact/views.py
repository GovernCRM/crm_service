from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .models import Contact, DynamicFormField
from .serializers import ContactSerializer, DynamicFormFieldSerializer
from .permissions import ContactPermission  # ContactPermission
from .serializers import ContactSerializer, DynamicFormFieldSerializer

class ContactViewSet(viewsets.ModelViewSet):
    """
    User's contacts.
    """

    def list(self, request):
        # Use this or the ordering filter won't work
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user_uuid = self.request.session.get('jwt_user_uuid')
        serializer.save(user_uuid=user_uuid)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(ContactViewSet, self).update(request, *args, **kwargs)

    @action(detail=False, methods=['GET'], url_path=r'state-record-contact/(?P<state_record_id>[^/]+)')
    def state_record_contact(self, request, *args, **kwargs):
        state_record_id = kwargs.get('state_record_id')
        try:
            serializer = ContactSerializer(
                Contact.objects.get(state_record_id=state_record_id),
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Contact.DoesNotExist:
            return Response({"error": "Contact not found"}, status=status.HTTP_404_NOT_FOUND)

    ordering_fields = ('first_name',)
    filter_backends = (filters.OrderingFilter,)
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DynamicFormFieldViewSet(viewsets.ModelViewSet):
    """
    Dynamic form fields for contacts.
    """
    queryset = DynamicFormField.objects.all()
    serializer_class = DynamicFormFieldSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('field_name',)
    ordering = ('field_name',)
    # def perform_create(self, serializer):
    #     user_uuid = self.request.session.get('jwt_user_uuid')
    #     serializer.save(user_uuid=user_uuid)
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(DynamicFormFieldViewSet, self).update(request, *args, **kwargs)


