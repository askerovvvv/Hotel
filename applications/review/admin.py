from django.contrib import admin

from applications.review.models import *

admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Comment)
