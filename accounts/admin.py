from django.contrib import admin
from .models import UserProfile, SupporterProfile, SupporterNote

admin.site.register(UserProfile)
admin.site.register(SupporterProfile)
admin.site.register(SupporterNote)
