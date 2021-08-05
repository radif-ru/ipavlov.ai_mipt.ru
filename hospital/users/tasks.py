from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from hospital.settings import DOCTOR
from users.models import TimeTable, HospitalUser, DoctorWorkingHours, \
    DoctorVacation


@shared_task
def generating_slots(time_step=20, quantity_days=7):
    """ Генерация слотов для врачей
    :param time_step: по умолчанию 1 слот - 20 минут
    :param quantity_days: по умолчанию на 7 дней вперёд
    """
    now = timezone.now()
    time_now = now.time()
    last_day = now + timedelta(days=quantity_days)

    doctors = HospitalUser.objects.filter(groups__name=DOCTOR)

    for doctor in doctors:
        working_hours = DoctorWorkingHours.objects.filter(
            doctor=doctor)

        if not working_hours:
            print(f'Для доктора {doctor.username} необходимо заполнить таблицу'
                  f' графика работы!')
            continue

        vacation = DoctorVacation.objects.filter(
            doctor=doctor, stop_time__gte=now).first()

        time_table = TimeTable.objects.filter(
            doctor=doctor, stop_time__gte=now).last()

        if time_table:
            new_start_time = time_table.stop_time
        else:
            if time_now.minute <= time_step:
                new_start_time = now + timedelta(
                    minutes=time_step - now.minute)
            elif time_now.minute <= time_step * 2:
                new_start_time = now + timedelta(
                    minutes=time_step * 2 - now.minute)
            else:
                new_start_time = now + timedelta(
                    minutes=time_step * 3 - now.minute)

        slots_list = []
        while new_start_time < last_day:
            new_weekday = new_start_time.weekday()
            new_stop_time = new_start_time + timedelta(minutes=time_step)

            if vacation:
                if vacation.start_time < new_start_time < vacation.stop_time:
                    new_start_time += timedelta(minutes=time_step)
                    continue

            working_hour = working_hours.filter(
                working_day=new_weekday).first()
            new_start_t = new_start_time.time()

            if not working_hour:
                new_start_time += timedelta(minutes=time_step)
                continue

            if not working_hour.start_time < new_start_t < working_hour.stop_time:
                new_start_time += timedelta(minutes=time_step)
                continue

            if working_hour.start_break_time and working_hour.stop_break_time:
                if working_hour.start_break_time < new_start_t < working_hour.stop_break_time:
                    new_start_time += timedelta(minutes=time_step)
                    continue

            new_time_table = TimeTable(
                doctor=doctor, start_time=new_start_time,
                stop_time=new_stop_time)
            slots_list.append(new_time_table)

            new_start_time += timedelta(minutes=time_step)

        TimeTable.objects.bulk_create(slots_list)
