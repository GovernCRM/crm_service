import uuid

from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db import models

from .validators import validate_emails, validate_phones, validate_addresses

from django.core.validators import RegexValidator

TITLE_CHOICES = (
    ('mr', 'Mr.'),
    ('ms', 'Ms.'),
)

CONTACT_TYPE_CHOICES = (
    ('customer', 'Customer'),
    ('supplier', 'Supplier'),
    ('producer', 'Producer'),
    ('personnel', 'Personnel'),
)

CUSTOMER_TYPE_CHOICES = (
    ('customer', 'Customer'),
    ('company', 'Company'),
    ('public', 'Public'),
)

ADDRESS_TYPE_CHOICES = (
    'home',
    'billing',
    'business',
    'delivery',
    'mailing',
)

PHONE_TYPE_CHOICES = (
    'office',
    'mobile',
    'home',
    'fax',
)

EMAIL_TYPE_CHOICES = (
    'office',
    'private',
    'other',
)


class ContactPreferenceChoices(models.TextChoices):
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    PHONE = 'phone', 'Phone'
    MAIL = 'mail', 'Mail'


class Contact(models.Model):
    contact_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user_uuid = models.UUIDField(blank=True, null=True)
    first_name = models.CharField(max_length=255, help_text='First name')
    middle_name = models.CharField(max_length=255, blank=True, null=True, help_text='Middle name ')
    last_name = models.CharField(max_length=255, help_text='Surname or family name')
    title = models.CharField(max_length=2, choices=TITLE_CHOICES, blank=True, null=True, help_text='Choices: {}'.format(", ".join([kv[0] for kv in TITLE_CHOICES])))
    contact_type = models.CharField(max_length=30, choices=CONTACT_TYPE_CHOICES, blank=True, null=True, help_text='Choices: {}'.format(", ".join([kv[0] for kv in CONTACT_TYPE_CHOICES])))
    customer_type = models.CharField(max_length=30, choices=CUSTOMER_TYPE_CHOICES, blank=True, null=True, help_text='Choices: {}'.format(", ".join([kv[0] for kv in CUSTOMER_TYPE_CHOICES])))
    company = models.CharField(max_length=100, blank=True, null=True)
    addresses = ArrayField(HStoreField(), blank=True, null=True, help_text="List of 'address' objects with the structure: type (string - Choices: {}),street (string), house_number (string), postal_code: (string), city (string), country (string)".format(", ".join([k for k in ADDRESS_TYPE_CHOICES])), validators=[validate_addresses])
    emails = ArrayField(HStoreField(), blank=True, null=True,help_text="List of 'email' objects with the structure: type (string - Choices: {}), email (string ".format(", ".join([k for k in EMAIL_TYPE_CHOICES])), validators=[validate_emails])
    phones = ArrayField(HStoreField(), blank=True, null=True, help_text="List of 'phone' objects with the structure: type (string - Choices: {}), number (string)".format(", ".join([k for k in PHONE_TYPE_CHOICES])), validators=[validate_phones])
    notes = models.TextField(blank=True, null=True)

    state = models.CharField(max_length=4, blank=True, null=True, help_text="State of the contact")
    state_record_id = models.UUIDField(unique=True, blank=True, null=True, help_text="Unique identifier of the state record")
    preferred_name = models.CharField(max_length=255, blank=True, null=True, help_text="Preferred name of the contact")
    prefix = models.CharField(max_length=10, blank=True, null=True, help_text="Prefix, e.g., Dr., Prof.")
    profession = models.CharField(max_length=254, blank=True, null=True, help_text="Profession of the contact")
    employer = models.CharField(max_length=254, blank=True, null=True, help_text="Employer of the contact")
    contact_preferences = ArrayField(base_field=models.CharField(max_length=30, choices=ContactPreferenceChoices.choices), blank=True, null=True, help_text="Contact preferences as a JSON object")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_index_serializer(self):
        from .serializers import ContactIndexSerializer
        return ContactIndexSerializer(self)


class Address(models.Model):
    street_num = models.CharField(max_length=10, validators=[RegexValidator(r'^\d+$', message="Street number must be numeric")])
    street_dir = models.CharField(max_length=2, blank=True, null=True, help_text="Directional prefix, e.g., N, S, E, W")
    street_name = models.CharField(max_length=100, help_text="Name of the street")
    street_type = models.CharField(max_length=20, blank=True, null=True, help_text="Type of the street, e.g., St, Ave, Blvd")
    street_post_dir = models.CharField(max_length=2, blank=True, null=True, help_text="Directional suffix, e.g., N, S, E, W")
    building_num = models.CharField(max_length=10, blank=True, null=True, help_text="Building or apartment number")
    city = models.CharField(max_length=100, help_text="City name")
    zip_code = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{5}(-\d{4})?$', message="Enter a valid ZIP code")])

    def __str__(self):
        return f"{self.street_num} {self.street_dir or ''} {self.street_name} {self.street_type or ''}, {self.city}, {self.zip_code}"


class FieldType(models.TextChoices):
    TEXT = 'text', 'Text'
    NUMBER = 'number', 'Number'
    DATE = 'date', 'Date'
    EMAIL = 'email', 'Email'
    PHONE = 'phone', 'Phone'
    ADDRESS = 'address', 'Address'
    SELECT = 'select', 'Select'
    CHECKBOX = 'checkbox', 'Checkbox'
    RADIO = 'radio', 'Radio'
    TEXTAREA = 'textarea', 'Textarea'

class DynamicFormField(models.Model):
    field_name = models.CharField(max_length=255, help_text="Name of the dynamic form field")
    field_type = models.CharField(max_length=50, help_text="Type of the dynamic form field", choices=FieldType.choices)
    field_label = models.CharField(max_length=255, help_text="Label for the dynamic form field")
    field_help_text = models.TextField(blank=True, null=True, help_text="Help text for the dynamic form field")
    field_options = ArrayField(models.CharField(max_length=255), blank=True, null=True, help_text="Options for select, checkbox, or radio fields")
    field_required = models.BooleanField(default=False, help_text="Is the field required?")
    field_placeholder = models.CharField(max_length=255, blank=True, null=True, help_text="Placeholder text for the field")
    field_default_value = models.TextField(blank=True, null=True, help_text="Default value for the field")
    field_value = models.TextField(blank=True, null=True, help_text="Value of the dynamic form field")
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='dynamic_fields', help_text="Related contact")

    def __str__(self):
        return f"{self.field_name}: {self.field_value}"



