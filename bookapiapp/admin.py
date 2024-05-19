from django.contrib import admin

from .models import Recommendation, UserInteraction

admin.site.register(Recommendation)
admin.site.register(UserInteraction)
