import functools

from django.contrib.auth.models import Group
from rest_framework import serializers

from hospital.settings import ADMINISTRATOR, DOCTOR
from users.models import HospitalUser, TimeTable


def is_admin_decorator(method):
    """
    Декоратор добавляет проверку для метода -
    является ли редактируемый пользователь администратором
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if Group.objects.get(name=ADMINISTRATOR) in args[1]['groups']:
            raise serializers.ValidationError(
                "Вы не имеете доступа к администраторам!")
        return method(self, *args, **kwargs)

    return wrapper


def is_doctor_decorator(method):
    """
    Декоратор добавляет проверку для метода -
    является ли редактируемый пользователь врачом
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if Group.objects.get(name=DOCTOR) in args[1]['groups']:
            raise serializers.ValidationError(
                "На приём можно записаться только к врачу!")
        return method(self, *args, **kwargs)

    return wrapper


class HospitalUserSerializer(serializers.ModelSerializer):
    """Создание, редактирование данных пациента или врача"""
    password = serializers.CharField(max_length=128, write_only=True)

    @is_admin_decorator
    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    @is_admin_decorator
    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = HospitalUser
        fields = ['username', 'password', 'last_name', 'first_name',
                  'middle_name', 'sex', 'birthdate', 'groups']


class HospitalUserBlockingSerializer(serializers.ModelSerializer):
    """Блокировка пациента или врача"""

    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        if not user.is_active:
            raise serializers.ValidationError("Пользователь уже заблокирован!")
        user.is_active = False
        user.save()
        return user

    class Meta:
        model = HospitalUser
        username = serializers.CharField(read_only=True)
        fields = []


class DoctorFreeSlotGetterSerializer(serializers.ModelSerializer):
    """Получение свободных слотов у врача в будущем"""

    class Meta:
        model = TimeTable
        fields = ['id', 'start_time', 'stop_time']


class AppointmentWithDoctorSerializer(serializers.ModelSerializer):
    """Возможность записи на приём к врачу (заполнение слота)"""

    class Meta:
        model = TimeTable
        fields = []

    def update(self, *args, **kwargs):
        slot = super().update(*args, **kwargs)
        if slot.client:
            raise serializers.ValidationError("Слот занят!")

        if self.context['request'].auth:
            client_id = self.context['request'].auth.payload['user_id']
            slot.client = HospitalUser.objects.get(pk=client_id)
        else:
            slot.client = self.context['request'].user

        slot.save()
        return slot


class UndoAppointmentWithDoctorSerializer(serializers.ModelSerializer):
    """Возможность отмены записи на приём"""

    def update(self, *args, **kwargs):
        slot = super().update(*args, **kwargs)

        if not slot.client:
            raise serializers.ValidationError("Слот не занят!")

        if self.context['request'].auth:
            client_id = self.context['request'].auth.payload['user_id']
            client = HospitalUser.objects.get(pk=client_id)
        else:
            client = self.context['request'].user

        if client == slot.client:
            slot.client = None
        else:
            raise serializers.ValidationError("Это не Ваш слот!")

        slot.save()
        return slot

    class Meta:
        model = TimeTable
        fields = []
