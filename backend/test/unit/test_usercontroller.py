
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


@pytest.mark.unit
def test_get_user_by_email_1_match():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = [user1]
    uc = UserController(dao=mockedDAO)

    assert uc.get_user_by_email(email='jane.doe@email.com') == user1


@pytest.mark.unit
def test_get_user_by_email_multiple_matches():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = [user1, user2]
    uc = UserController(dao=mockedDAO)

    assert uc.get_user_by_email(email='jane.doe@email.com') == user1


@pytest.mark.unit
def test_get_user_by_email_0_matches():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = []
    uc = UserController(dao=mockedDAO)

    assert uc.get_user_by_email(email='jane.doe@email.com') == None


@pytest.mark.unit
def test_get_user_by_email_invalid_email():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = []
    uc = UserController(dao=mockedDAO)

    with pytest.raises(ValueError):
        uc.get_user_by_email(email='jane.doe')


@pytest.mark.unit
def test_get_user_by_email_db_failure():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.side_effect = Exception("Database error")
    uc = UserController(dao=mockedDAO)

    with pytest.raises(Exception) as exc_info:
        uc.get_user_by_email(email='jane.doe@email.com')

    assert "Database error" in str(exc_info.value)