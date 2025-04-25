
import pytest
import unittest.mock as mock
from unittest.mock import patch
from src.controllers.usercontroller import UserController


@pytest.fixture
def user1():
    return {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@email.com'}

@pytest.fixture
def user2():
    return {'firstName': 'Janet', 'lastName': 'Doeg', 'email': 'jane.doe@email.com'}


def test_get_user_by_email_1_match():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = [user1]
    uc = UserController(dao=mockedDAO)

    assert uc.get_user_by_email(email='jane.doe@email.com') == user1


def test_get_user_by_email_multiple_matches():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = [user1, user2]
    uc = UserController(dao=mockedDAO)

    assert uc.get_user_by_email(email='jane.doe@email.com') == user1


def test_get_user_by_email_0_matches():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = []
    uc = UserController(dao=mockedDAO)

    assert uc.get_user_by_email(email='jane.doe@email.com') == None


def test_get_user_by_email_invalid_email():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = []
    uc = UserController(dao=mockedDAO)

    with pytest.raises(ValueError):
        uc.get_user_by_email(email='jane.doe')