from django.db.models import Count
from django.utils.datetime_safe import datetime
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView

from hospital.settings import ADMINISTRATOR, PATIENT
from .models import HospitalUser, TimeTable
from .permissions import HasGroupPermission
from .serializers import HospitalUserSerializer, \
    HospitalUserBlockingSerializer, \
    DoctorFreeSlotGetterSerializer, AppointmentWithDoctorSerializer, \
    UndoAppointmentWithDoctorSerializer


class AdminPermissionsMixin:
    """Права администратора при обновлении данных"""
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': [ADMINISTRATOR],
        'PUT': [ADMINISTRATOR],
        'PATCH': [ADMINISTRATOR],
        'HEAD': [ADMINISTRATOR],
        'OPTIONS': [ADMINISTRATOR],
    }


class PatientPermissionsMixin:
    """Права пациента при обновлении данных"""
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': [PATIENT],
        'PUT': [PATIENT],
        'PATCH': [PATIENT],
        'HEAD': [PATIENT],
        'OPTIONS': [PATIENT],
    }


class HospitalUserCreateView(generics.CreateAPIView):
    """Создание пациента или врача"""
    queryset = HospitalUser.objects.exclude(
        groups__name__contains=ADMINISTRATOR)
    serializer_class = HospitalUserSerializer

    permission_classes = [HasGroupPermission]
    required_groups = {
        'POST': [ADMINISTRATOR],
        'OPTIONS': [ADMINISTRATOR],
    }


class HospitalUserUpdateView(AdminPermissionsMixin,
                             generics.RetrieveUpdateAPIView):
    """Изменение данных пациента или врача"""
    queryset = HospitalUser.objects.exclude(
        groups__name__contains=ADMINISTRATOR)
    serializer_class = HospitalUserSerializer


class HospitalUserBlockingView(AdminPermissionsMixin, generics.UpdateAPIView):
    """Блокировка пациента или врача"""
    queryset = HospitalUser.objects.exclude(
        groups__name__contains=ADMINISTRATOR)
    serializer_class = HospitalUserBlockingSerializer


class DoctorFreeSlotGetterView(generics.ListAPIView):
    """Получение свободных слотов у врача в будущем"""
    queryset = TimeTable.objects.all()
    serializer_class = DoctorFreeSlotGetterSerializer
    permission_classes = [permissions.IsAuthenticated]
    date_time_now = datetime.now()

    def get_queryset(self, *args, **kwargs):
        doctor_id = self.request.parser_context['kwargs']['pk']
        return self.queryset.filter(
            doctor_id=doctor_id, client_id__isnull=True,
            start_time__gte=self.date_time_now,
            stop_time__gte=self.date_time_now)


class AppointmentWithDoctor(PatientPermissionsMixin, generics.UpdateAPIView):
    """Возможность записи на приём к врачу (заполнение слота)"""
    queryset = TimeTable.objects.all()
    serializer_class = AppointmentWithDoctorSerializer


class UndoAppointmentWithDoctor(PatientPermissionsMixin,
                                generics.UpdateAPIView):
    """Возможность отмены записи на приём"""
    queryset = TimeTable.objects.all()
    serializer_class = UndoAppointmentWithDoctorSerializer


class AllEntries(APIView):
    """Получение статистических данных: сколько записей на какой день"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        queryset = TimeTable.objects.values('start_time__date').annotate(
            count=Count('pk'))
        queryset.query.values_select = ('day',)
        return Response(queryset)
