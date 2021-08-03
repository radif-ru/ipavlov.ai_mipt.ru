from django.urls import resolve

from rest_framework.reverse import reverse


class TestUrls:
    """Тестирование доступности url-адресов"""
    test_pk = {'pk': 1}

    def test_token_url(self):
        """Авторизация по токену JWT"""
        path = reverse('token_obtain_pair')
        assert resolve(path).view_name == 'token_obtain_pair'

    def test_token_refresh_url(self):
        """Обновление токена JWT"""
        path = reverse('token_refresh')
        assert resolve(path).view_name == 'token_refresh'

    def test_user_create_url(self):
        """Создание пациента или врача"""
        path = reverse('user-create')
        assert resolve(path).view_name == 'user-create'

    def test_user_update_url(self):
        """Изменение данных пациента или врача"""
        path = reverse('user-update', kwargs=self.test_pk)
        assert resolve(path).view_name == 'user-update'

    def test_user_blocking_url(self):
        """Блокировка пациента или врача"""
        path = reverse('user-blocking', kwargs=self.test_pk)
        assert resolve(path).view_name == 'user-blocking'

    def test_doctor_slots_get_url(self):
        """Получение свободных слотов у врача в будущем"""
        path = reverse('get-slots', kwargs=self.test_pk)
        assert resolve(path).view_name == 'get-slots'

    def test_doctor_appointment_url(self):
        """Возможность записи на приём к врачу (заполнение слота)"""
        path = reverse('doctor-appointment', kwargs=self.test_pk)
        assert resolve(path).view_name == 'doctor-appointment'

    def test_doctor_appointment_undo_url(self):
        """Возможность отмены записи на приём"""
        path = reverse('undo-doctor-appointment', kwargs=self.test_pk)
        assert resolve(path).view_name == 'undo-doctor-appointment'

    def test_doctor_entries_all_url(self):
        """Получение статистических данных: сколько записей на какой день"""
        path = reverse('doctor-all-entries')
        assert resolve(path).view_name == 'doctor-all-entries'
