from django.db.models import Count
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView

from hospital.settings import ADMINISTRATOR, PATIENT
from .models import HospitalUser, TimeTable
from .permissions import HasGroupPermission
from .serializers import HospitalUserSerializer, HospitalUserBlockingSerializer, \
    DoctorFreeSlotGetterSerializer, AppointmentWithDoctorSerializer, \
    UndoAppointmentWithDoctorSerializer


class HospitalUserCreateView(generics.CreateAPIView):
    queryset = HospitalUser.objects.all()
    serializer_class = HospitalUserSerializer

    permission_classes = [HasGroupPermission]
    required_groups = {
        'POST': [ADMINISTRATOR],
        'OPTIONS': [ADMINISTRATOR],
    }


class HospitalUserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = HospitalUser.objects.get_queryset()
    serializer_class = HospitalUserSerializer

    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': [ADMINISTRATOR],
        'PUT': [ADMINISTRATOR],
        'PATCH': [ADMINISTRATOR],
        'HEAD': [ADMINISTRATOR],
        'OPTIONS': [ADMINISTRATOR],
    }


class HospitalUserBlockingView(generics.UpdateAPIView):
    queryset = HospitalUser.objects.all()
    serializer_class = HospitalUserBlockingSerializer

    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': [ADMINISTRATOR],
        'PUT': [ADMINISTRATOR],
        'PATCH': [ADMINISTRATOR],
        'HEAD': [ADMINISTRATOR],
        'OPTIONS': [ADMINISTRATOR],
    }


class DoctorFreeSlotGetterView(generics.ListAPIView):
    queryset = TimeTable.objects.all()
    serializer_class = DoctorFreeSlotGetterSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        doctor_id = self.request.parser_context['kwargs']['pk']
        return self.queryset.filter(doctor_id=doctor_id, client_id__isnull=True)


class AppointmentWithDoctor(generics.UpdateAPIView):
    queryset = TimeTable.objects.get_queryset()
    serializer_class = AppointmentWithDoctorSerializer

    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': [PATIENT],
        'PUT': [PATIENT],
        'PATCH': [PATIENT],
        'HEAD': [PATIENT],
        'OPTIONS': [PATIENT],
    }


class UndoAppointmentWithDoctor(generics.UpdateAPIView):
    queryset = TimeTable.objects.get_queryset()
    serializer_class = UndoAppointmentWithDoctorSerializer

    permission_classes = [permissions.AllowAny]
    required_groups = {
        'GET': [PATIENT],
        'PUT': [PATIENT],
        'PATCH': [PATIENT],
        'HEAD': [PATIENT],
        'OPTIONS': [PATIENT],
    }


class AllEntries(APIView):
    permission_classes = [HasGroupPermission]

    def get(self, request):
        queryset = TimeTable.objects.values('start_time__date').annotate(
            count=Count('pk'))
        queryset.query.values_select = ('day',)
        return Response(queryset)
