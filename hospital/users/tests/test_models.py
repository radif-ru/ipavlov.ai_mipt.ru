from mixer.backend.django import mixer
import pytest

from users.models import HospitalUser


@pytest.mark.django_db
class TestModels:
    """Тестирование моделей"""
    user_name = 'jenya'
    password = 'qwerty'
    model = HospitalUser

    def test_hospital_user_is_in_stock(self):
        """Тестирование модели пользователей"""
        hospital_user = mixer.blend(
            self.model, username=self.user_name, password=self.password)

        assert isinstance(hospital_user, HospitalUser)
        assert hospital_user.__str__() == self.user_name
