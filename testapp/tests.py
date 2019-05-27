# content of test_sample.py
import pytest

from testapp import views

pytestmark = pytest.mark.django_db


def test_get_user(db_setup):
    assert views.get_user('test').name == 'test'
