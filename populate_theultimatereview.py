import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from ultimatereview.models import Review, Researcher, Query, Paper

def populate():

    example_user1 = ('jill')

    add_user()
