import os

from django.core.management.base import BaseCommand

from django.contrib.auth.models import Group
from django.db import OperationalError, ProgrammingError

from hospital.settings import ADMINISTRATOR, PATIENT, DOCTOR
from users.models import HospitalUser


class Command(BaseCommand):
    help = 'Create admin and groups'

    def handle(self, *args, **options):
        self.create_admin()
        self.create_groups()

    def create_admin(self):
        """Создание супер-юзера"""
        try:
            if not HospitalUser.objects.exists():
                HospitalUser.objects.create_superuser(
                    username='admin',
                    email='admin@local.ru',
                    password='medicalqwerty')
        except Exception:
            self.migrate()
            self.collect_static()
            self.create_admin()

    def create_groups(self):
        try:
            if not Group.objects.exists():
                Group.objects.create(
                    name=ADMINISTRATOR,
                )
                Group.objects.create(
                    name=PATIENT
                )
                Group.objects.create(
                    name=DOCTOR
                )
        except OperationalError or ProgrammingError:
            self.create_admin()

    @staticmethod
    def migrate():
        os.system('python manage.py makemigrations --noinput')
        os.system('python manage.py migrate --noinput')

    @staticmethod
    def collect_static():
        """Сборка стандартных и подготовленных статических файлов"""
        os.system('python manage.py collectstatic --no-input --clear')
