from django.contrib import admin
from .models import Topic, Subscriber, Content

admin.site.register(Topic)
admin.site.register(Subscriber)
admin.site.register(Content)