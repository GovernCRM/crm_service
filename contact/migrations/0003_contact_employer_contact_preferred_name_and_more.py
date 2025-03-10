# Generated by Django 5.1.5 on 2025-03-10 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_alter_contact_addresses_alter_contact_emails_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='employer',
            field=models.CharField(blank=True, help_text='Employer of the contact', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='preferred_name',
            field=models.CharField(blank=True, help_text='Preferred name of the contact', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='prefix',
            field=models.CharField(blank=True, help_text='Prefix, e.g., Dr., Prof.', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='profession',
            field=models.CharField(blank=True, help_text='Profession of the contact', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='state',
            field=models.CharField(blank=True, help_text='State of the contact', max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='state_record_id',
            field=models.UUIDField(blank=True, help_text='Unique identifier of the state record', null=True, unique=True),
        ),
    ]
