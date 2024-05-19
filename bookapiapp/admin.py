from django.contrib import admin

from .models import Book, UserInteraction

admin.site.register(Book)
admin.site.register(UserInteraction)
