from django.contrib import admin

from groups.models import Group, Member

# Register your models here.

admin.site.register(Group)
admin.site.register(Member)
