from rest_framework import serializers

from users.models import HospitalUser, TimeTable


class HospitalUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

    class Meta:
        model = HospitalUser
        fields = ['username', 'password', 'last_name', 'first_name',
                  'middle_name', 'sex', 'birthdate', 'groups']


class HospitalUserBlockingSerializer(serializers.ModelSerializer):
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


class DoctorTimeTableSerializer(serializers.ModelSerializer):
    user = HospitalUserSerializer()

    class Meta:
        model = TimeTable
        fields = ['__all__']


class DoctorFreeSlotGetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = ['id', 'start_time', 'stop_time']


class AppointmentWithDoctorSerializer(serializers.ModelSerializer):
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
