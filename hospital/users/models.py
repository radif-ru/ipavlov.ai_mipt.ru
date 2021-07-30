from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import date


class HospitalUser(AbstractUser):
    SEX_CHOICES = [
        ('м', 'Мужской'),
        ('ж', 'Женский')
    ]

    middle_name = models.CharField('отчество', max_length=300)
    sex = models.CharField(
        choices=SEX_CHOICES, default=1, max_length=1, verbose_name='Пол'
    )
    birthdate = models.DateField(
        max_length=8, verbose_name='Дата рождения', default='2003-01-01'
    )

    def __str__(self):
        return f'{self.username} - {self.last_name} {self.first_name} ' \
               f'{self.middle_name} - {self.birthdate}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name', 'middle_name', 'birthdate']


class TimeTable(models.Model):
    STATE_CHOICES = (
        ('1', 'Прием'),
        ('2', 'Перерыв'),
        ('3', 'Отпуск'),
    )

    state = models.CharField(
        'Статус', max_length=1, choices=STATE_CHOICES, default=''
    )
    doctor = models.ForeignKey(
        HospitalUser, verbose_name='Врач', on_delete=models.SET_NULL,
        blank=True, null=True, related_name='doctor'
    )
    client = models.ForeignKey(
        HospitalUser, verbose_name='Пациент', on_delete=models.SET_NULL,
        blank=True, null=True, related_name='patient'
    )
    date = models.DateField('Дата', default=date.today)
    start_time = models.TimeField('Начало', blank=True, null=True)
    stop_time = models.TimeField('Окончание', blank=True, null=True)

    class Meta:
        verbose_name = 'Время работы врача'
        verbose_name_plural = 'Время работы врачей'
