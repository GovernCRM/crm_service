#!/usr/bin/env bash

set -e

echo $(date -u) "- Migrating"
python manage.py makemigrations
python manage.py migrate

# export env variable from file
if [ -e /JWT_PRIVATE_KEY_RSA_BUILDLY ]
then
  export JWT_PRIVATE_KEY_RSA_BUILDLY=`cat /JWT_PRIVATE_KEY_RSA_BUILDLY`
fi

if [ -e /JWT_PUBLIC_KEY_RSA_BUILDLY ]
then
  export JWT_PUBLIC_KEY_RSA_BUILDLY=`cat /JWT_PUBLIC_KEY_RSA_BUILDLY`
fi

echo $(date -u) "- Collect Static"
python manage.py collectstatic --no-input

echo $(date -u) "- Creating admin user"
python manage.py shell -c "import os; from django.contrib.auth.models import User; User.objects.filter(email=os.getenv('DJANGO_SUPERUSER_EMAIL')).delete(); User.objects.create_superuser(os.getenv('DJANGO_SUPERUSER_USERNAME'), os.getenv('DJANGO_SUPERUSER_EMAIL'), os.getenv('DJANGO_SUPERUSER_PASSWORD'))"

echo $(date -u) "- Running the server"
gunicorn -b 0.0.0.0:8080 crm_service.wsgi
