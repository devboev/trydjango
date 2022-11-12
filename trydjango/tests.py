from django.test import TestCase
from django.conf import settings
from django.contrib.auth.password_validation import validate_password


class TryDjangoConfigTest(TestCase):
    # https://docs.python.org/3/library/unittest.html
    def test_secret_key_strength(self):
        # print('vxcv',validate_password(settings.SECRET_KEY))
        # self.assertNotEqual(settings.SECRET_KEY,'abc123')
        try:
            is_strong=validate_password(settings.SECRET_KEY)
            print('strong')
        except Exception as e:
            msg = f'Bad Secret Key {e.messages}'
            self.fail(msg)