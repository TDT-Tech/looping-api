from django.contrib import admin

from newsletters.models import Answer, Newsletter, Question

admin.site.register(Newsletter)
admin.site.register(Question)
admin.site.register(Answer)
