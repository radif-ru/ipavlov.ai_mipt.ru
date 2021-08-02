from django.contrib import admin

from .models import HospitalUser, TimeTable, DoctorWorkingHours, DoctorVacation

admin.site.register(HospitalUser)
admin.site.register(DoctorWorkingHours)
admin.site.register(DoctorVacation)
admin.site.register(TimeTable)
