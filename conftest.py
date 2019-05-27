import pytest

from testapp import models


@pytest.fixture
def db_setup():
    user = models.User(name='test')
    user.save()
