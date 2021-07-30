from django.contrib import admin

from users.models import HospitalUser, TimeTable

admin.site.register(HospitalUser)
admin.site.register(TimeTable)
