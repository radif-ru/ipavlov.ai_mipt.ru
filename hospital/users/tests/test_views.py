import json

import pytest
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from users.models import HospitalUser, TimeTable


@pytest.mark.django_db
class TestViews:
    """Тестирование представлений"""
    test_pk = {'pk': 1}
    test_pk_int = 1

    def test_get_slots(self, client, create_test_user, user_data, login_data,
                       authenticated_user):
        """Получение свободных слотов в будущем авторизованным пользователем"""
        mixer.blend(TimeTable, client_id=None, doctor_id=self.test_pk_int,
                    start_time='2023-08-31T15:57:45+03:00',
                    stop_time='2023-08-31T16:57:59+03:00')
        mixer.blend(TimeTable, client=None, doctor_id=self.test_pk_int,
                    start_time='2023-08-31 12:57:45+00:00',
                    stop_time='2023-08-31 12:57:45+00:00')
        mixer.blend(TimeTable, client=None, doctor_id=self.test_pk_int,
                    start_time='2023-08-31',
                    stop_time='2023-08-31')

        path = reverse('get-slots', kwargs=self.test_pk)
        response = client.get(path, pk=self.test_pk)
        assert response.status_code == 200

        data_in_page = json.loads(response.content.decode())
        assert isinstance(data_in_page[0], dict)
        assert len(data_in_page) == 3
        assert response.content == \
               '[{"id":1,"start_time":"2023-08-31T15:57:45+03:00",' \
               '"stop_time":"2023-08-31T16:57:59+03:00"},' \
               '{"id":2,"start_time":"2023-08-31T15:57:45+03:00",' \
               '"stop_time":"2023-08-31T15:57:45+03:00"},' \
               '{"id":3,"start_time":"2023-08-31T00:00:00+03:00",' \
               '"stop_time":"2023-08-31T00:00:00+03:00"}]'.encode()

    def test_all_entries(self, client):
        """Получение статистических данных: сколько записей на какой день"""
        mixer.blend(TimeTable)
        mixer.blend(TimeTable)
        mixer.blend(TimeTable)
        path = reverse('doctor-all-entries')
        response = client.get(path)
        assert response.status_code == 200

        data_in_page = json.loads(response.content.decode())
        assert isinstance(data_in_page[0], dict)
        assert len(data_in_page) == 3

    def test_create_and_authenticated(
            self, client, create_test_user, user_data, login_data,
            authenticated_user):
        """Тестирование создания и аутентификации пользователей"""
        user_model = HospitalUser
        user = create_test_user
        assert user_model.objects.count() == 1
        assert isinstance(user, user_model)

        user = authenticated_user
        assert user.is_authenticated
