import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ultimate_review.settings')

import django
django.setup()

from django.contrib.auth.models import User
from ultimatereview.models import Review, Researcher, Query, Paper

def populate():

    user1 = User.objects.create_user(username='jill', email='jill@email.com', password='jill')
    user1.save()
    user2 = User.objects.create_user(username='jim', email='jim@email.com', password='jim')
    user2.save()
    user3 = User.objects.create_user(username='joe', email='joe@email.com', password='joe')
    user3.save()
    user4 = User.objects.create_user(username='bob', email='bob@email.com', password='bob')
    user4.save()
    
    for u in User.objects.all():
        print "{0}".format(str(u))

if __name__ == '__main__':
    print "Starting The Ultimate Review population script..."
    populate()
