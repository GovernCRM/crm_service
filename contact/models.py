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


class Contact(models.Model):
    contact_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user_uuid = models.UUIDField(blank=True, null=True)
    first_name = models.CharField(max_length=255, help_text='First name')
    middle_name = models.CharField(max_length=255, blank=True, null=True, help_text='Middle name ')
    last_name = models.CharField(max_length=255, help_text='Surname or family name')
    title = models.CharField(max_length=2, choices=TITLE_CHOICES, blank=True, null=True,
                             help_text='Choices: {}'.format(", ".join([kv[0] for kv in TITLE_CHOICES])))
    contact_type = models.CharField(max_length=30, choices=CONTACT_TYPE_CHOICES, blank=True, null=True,
                                    help_text='Choices: {}'.format(", ".join([kv[0] for kv in CONTACT_TYPE_CHOICES])))
    customer_type = models.CharField(max_length=30, choices=CUSTOMER_TYPE_CHOICES, blank=True, null=True,
                                     help_text='Choices: {}'.format(", ".join([kv[0] for kv in CUSTOMER_TYPE_CHOICES])))
    company = models.CharField(max_length=100, blank=True, null=True)
    addresses = ArrayField(HStoreField(), blank=True, null=True,
                           help_text="""
                           List of 'address' objects with the structure:
                           type (string - Choices: {}),
                           street (string),
                           house_number (string),
                           postal_code: (string),
                           city (string),
                           country (string)
                           """.format(", ".join([k for k in
                                                 ADDRESS_TYPE_CHOICES])),
                           validators=[validate_addresses])
    emails = ArrayField(HStoreField(), blank=True, null=True,
                        help_text="""
                               List of 'email' objects with the structure:
                               type (string - Choices: {}),
                               email (string)
                               """.format(", ".join([k for k in
                                                     EMAIL_TYPE_CHOICES])),
                        validators=[validate_emails])
    phones = ArrayField(HStoreField(), blank=True, null=True,
                        help_text="""
                               List of 'phone' objects with the structure:
                               type (string - Choices: {}),
                               number (string)
                               """.format(", ".join([k for k in
                                                     PHONE_TYPE_CHOICES])),
                        validators=[validate_phones])
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_index_serializer(self):
        from .serializers import ContactIndexSerializer
        return ContactIndexSerializer(self)


class Address(models.Model):
    street_num = models.CharField(max_length=10,
                                  validators=[RegexValidator(r'^\d+$', message="Street number must be numeric")])
    street_dir = models.CharField(max_length=2, blank=True, null=True, help_text="Directional prefix, e.g., N, S, E, W")
    street_name = models.CharField(max_length=100, help_text="Name of the street")
    street_type = models.CharField(max_length=20, blank=True, null=True,
                                   help_text="Type of the street, e.g., St, Ave, Blvd")
    street_post_dir = models.CharField(max_length=2, blank=True, null=True,
                                       help_text="Directional suffix, e.g., N, S, E, W")
    building_num = models.CharField(max_length=10, blank=True, null=True, help_text="Building or apartment number")
    city = models.CharField(max_length=100, help_text="City name")
    zip_code = models.CharField(max_length=10,
                                validators=[RegexValidator(r'^\d{5}(-\d{4})?$', message="Enter a valid ZIP code")])

    def __str__(self):
        return f"{self.street_num} {self.street_dir or ''} {self.street_name} {self.street_type or ''}, {self.city}, {self.zip_code}"


class StateRecord(models.Model):
    STATE_CHOICES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
        ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'),
        ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
        ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'),
        ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'),
        ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
        ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
        ('PR', 'Puerto Rico')
    ]

    TYPE_CHOICES = [
        ('Person', 'Person'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          help_text="Unique identifier for the state record")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Person', help_text="Type of record")
    original_state = models.CharField(max_length=2, choices=STATE_CHOICES,
                                      help_text="State where the record originates")

    precinct = models.CharField(max_length=6, help_text="Precinct code")
    last_name = models.CharField(max_length=100, help_text="Last name of the person")
    first_name = models.CharField(max_length=100, help_text="First name of the person")
    middle_name = models.CharField(max_length=100, blank=True, null=True, help_text="Middle name of the person")
    suffix = models.CharField(max_length=10, blank=True, null=True, help_text="Suffix, e.g., Jr., Sr., III")
    voter_id = models.CharField(max_length=20, unique=True, help_text="Unique voter identification number")
    political_affiliation = models.CharField(max_length=10, choices=[
        ('DEM', 'Democratic'),
        ('REP', 'Republican'),
        ('IND', 'Independent'),
        ('OTH', 'Other')
    ], help_text="Political party affiliation")
    status = models.CharField(max_length=1, choices=[
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('R', 'Removed')
    ], help_text="Voter status")

    residential_address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name="residential_record",
                                               help_text="Residential address")
    mailing_address = models.OneToOneField(Address, on_delete=models.SET_NULL, blank=True, null=True,
                                           related_name="mailing_record", help_text="Mailing address")

    date_of_birth = models.DateField(help_text="Date of birth of the person")
    registration_date = models.DateField(blank=True, null=True, help_text="Date the person registered")

    muni = models.CharField(max_length=100, blank=True, null=True, help_text="Municipality of the person")
    muni_sub = models.CharField(max_length=100, blank=True, null=True, help_text="Subdivision of the municipality")
    school = models.CharField(max_length=100, blank=True, null=True, help_text="School district of the person")
    school_sub = models.CharField(max_length=100, blank=True, null=True, help_text="Subdivision of the school district")
    tech_center = models.CharField(max_length=100, blank=True, null=True, help_text="Technology center of the person")
    tech_center_sub = models.CharField(max_length=100, blank=True, null=True,
                                       help_text="Subdivision of the technology center")
    county_comm = models.CharField(max_length=100, blank=True, null=True, help_text="County commission district")

    voter_history = models.JSONField(blank=True, null=True, help_text="Historical voting data as a JSON object")

    county_desc = models.CharField(max_length=100, help_text="Description of the county")
    returned_undeliverable = models.BooleanField(default=False, help_text="Whether mail was returned as undeliverable")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.voter_id})"
