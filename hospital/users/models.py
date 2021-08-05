from django.contrib.auth.models import AbstractUser
from django.db import models


class HospitalUser(AbstractUser):
    """Пользователь больницы"""
    SEX_CHOICES = [
        ('м', 'Мужской'),
        ('ж', 'Женский')
    ]

    middle_name = models.CharField('отчество', max_length=150, blank=True)
    sex = models.CharField(
        choices=SEX_CHOICES, default='м', max_length=1, verbose_name='Пол'
    )
    birthdate = models.DateField(
        max_length=8, verbose_name='Дата рождения', default='2003-01-01'
    )

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name', 'middle_name', 'birthdate']


class DoctorWorkingHours(models.Model):
    """Рабочее время у доктора"""
    WORKING_DAY_CHOICES = (
        ('0', 'пн'),
        ('1', 'вт'),
        ('2', 'ср'),
        ('3', 'чт'),
        ('4', 'пт'),
        ('5', 'сб'),
        ('6', 'вс'),
    )

    doctor = models.ForeignKey(
        HospitalUser, verbose_name='Врач', on_delete=models.CASCADE
    )
    working_day = models.CharField(
        verbose_name='Рабочий день', max_length=2, choices=WORKING_DAY_CHOICES)

    start_time = models.TimeField(verbose_name='Начало')
    stop_time = models.TimeField(verbose_name='Окончание')

    start_break_time = models.TimeField(
        verbose_name='Начало обеда', blank=True, null=True
    )
    stop_break_time = models.TimeField(
        verbose_name='Окончание обеда', blank=True, null=True
    )

    def __str__(self):
        return f'{self.doctor}. W {self.get_working_day_display()} - ' \
               f'{self.start_time} - {self.stop_time}. ' \
               f'B {self.start_break_time} - {self.stop_break_time}'

    class Meta:
        verbose_name = 'Рабочее время врача'
        verbose_name_plural = 'Рабочее время врачей'
        unique_together = (('doctor', 'working_day'),)
        ordering = ['working_day', 'start_time']


class DoctorVacation(models.Model):
    """Отпуска у доктора"""
    doctor = models.ForeignKey(
        HospitalUser, verbose_name='Врач', on_delete=models.CASCADE
    )

    start_time = models.DateTimeField(verbose_name='Начало')
    stop_time = models.DateTimeField(verbose_name='Окончание')

    def __str__(self):
        return f'{self.doctor}. {self.start_time} - {self.stop_time}'

    class Meta:
        verbose_name = 'Отпуск у врача'
        verbose_name_plural = 'Отпуска у врачей'
        ordering = ['stop_time']


class TimeTable(models.Model):
    """Слоты, свободные промежутки времени для приёма пациентов"""
    doctor = models.ForeignKey(
        HospitalUser, verbose_name='Врач', on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        HospitalUser, verbose_name='Пациент', on_delete=models.SET_NULL,
        blank=True, null=True, related_name='patient'
    )

    start_time = models.DateTimeField(verbose_name='Начало')
    stop_time = models.DateTimeField(verbose_name='Окончание')

    def __str__(self):
        return f'{self.doctor}. {self.start_time} - {self.stop_time}'

    class Meta:
        verbose_name = 'Слот'
        verbose_name_plural = 'Слоты'
        ordering = ['stop_time']
