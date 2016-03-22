from django.contrib import admin
from ultimatereview.models import UserProfile
from ultimatereview.models import Researcher, Review, Query, Paper

class ReviewAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('pk','title')

class QueryAdmin(admin.ModelAdmin):
    list_display = ('pk','review')

class PaperAdmin(admin.ModelAdmin):
    list_display = ('pk','review','title','abstract_relevance','document_relevance')

admin.site.register(Researcher)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Query, QueryAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(UserProfile)
