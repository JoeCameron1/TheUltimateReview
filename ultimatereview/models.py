from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import date

class Researcher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.user_name

class Review(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=30, null=True)
    date_started = models.DateField()
    query_string = models.CharField(max_length=30, default="")
    pool_size = models.IntegerField(default=0)
    abstracts_judged = models.IntegerField(default=0)
    document_judged = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Review, self).save(*args, **kwargs)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.title or ''

class Query(models.Model):
    review = models.ForeignKey(Review)
    name = models.CharField(max_length=600,null = True)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.name or ''

class Paper(models.Model):
    review = models.ForeignKey(Review)
    title = models.CharField(max_length=30)
    authors = models.CharField(max_length=30)
    abstract = models.CharField(max_length=300)
    paper_url = models.URLField()
	full_text = models.URLField(null=True)
    abstract_relevance = models.CharField(max_length=30)
    document_relevance = models.CharField(max_length=30)
    notes = models.CharField(max_length=30)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.title or ''

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
