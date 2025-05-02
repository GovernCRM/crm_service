from rest_framework import serializers
from .models import Contact, ContactPreferenceChoices, DynamicFormField


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    organization_uuid = serializers.ReadOnlyField()

    class Meta:
        model = Contact
        exclude = ('user_uuid',)

    def validate_type(self, value):
        if not value:
            raise serializers.ValidationError(
                "type must be an array of one or more string elements"
            )
        return value


class ContactNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('contact_uuid', 'first_name', 'middle_name', 'last_name')


class ContactIndexSerializer(serializers.ModelSerializer):
    """
    Serializer for saving to ElasticSearchIndex.
    """
    organization_uuid = serializers.ReadOnlyField()

    class Meta:
        model = Contact
        fields = '__all__'

class DynamicFormFieldSerializer(serializers.ModelSerializer):
    """
    Serializer for DynamicFormField model.
    """
    class Meta:
        model = DynamicFormField
        fields = '__all__'
    extra_kwargs = {
        'id': {'read_only': True},
        'contact': {'required': False},
    }
    def create(self, validated_data):
        """
        Create a new DynamicFormField instance.
        """
        return DynamicFormField.objects.create(**validated_data)
    def update(self, instance, validated_data):
        """
        Update an existing DynamicFormField instance.
        """
        instance.field_name = validated_data.get('field_name', instance.field_name)
        instance.field_type = validated_data.get('field_type', instance.field_type)
        instance.field_value = validated_data.get('field_value', instance.field_value)
        instance.save()
        return instance
    def validate(self, data):
        """
        Validate the data for DynamicFormField.
        """
        if not data.get('field_name'):
            raise serializers.ValidationError("Field name is required.")
        if not data.get('field_type'):
            raise serializers.ValidationError("Field type is required.")
        if not data.get('field_value'):
            raise serializers.ValidationError("Field value is required.")
        return data



