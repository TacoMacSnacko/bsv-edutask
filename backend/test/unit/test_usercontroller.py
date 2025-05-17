
import pytest
import unittest.mock as mock
import sys
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
def test_get_user_by_email_multiple_matches(capsys):
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = [user1, user2]
    uc = UserController(dao=mockedDAO)
    
    returnedUser = uc.get_user_by_email(email='jane.doe@email.com')
    out, err = capsys.readouterr()

    # capsys.readouterr consumes the text from the stream, output it back into the stream.
    sys.stdout.write(out)
    sys.stdout.write(err)

    isUser1 = returnedUser == user1
    havePrintedEmail = 'jane.doe@email.com' in out

    assert isUser1 and havePrintedEmail


@pytest.mark.unit
def test_get_user_by_email_0_matches():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = []
    uc = UserController(dao=mockedDAO)

    assert uc.get_user_by_email(email='jane.doe@email.com') == None


@pytest.mark.unit
def test_get_user_by_email_invalid_email_missing_local():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = []
    uc = UserController(dao=mockedDAO)

    with pytest.raises(ValueError):
        uc.get_user_by_email(email='@email.com')


@pytest.mark.unit
def test_get_user_by_email_invalid_email_missing_at():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = []
    uc = UserController(dao=mockedDAO)

    with pytest.raises(ValueError):
        uc.get_user_by_email(email='jane.doeemail.com')


@pytest.mark.unit
def test_get_user_by_email_invalid_email_missing_domain():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = []
    uc = UserController(dao=mockedDAO)

    with pytest.raises(ValueError):
        uc.get_user_by_email(email='jane.doe@.com')


@pytest.mark.unit
def test_get_user_by_email_invalid_email_missing_dot():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = []
    uc = UserController(dao=mockedDAO)

    with pytest.raises(ValueError):
        uc.get_user_by_email(email='jane.doe@emailcom')


@pytest.mark.unit
def test_get_user_by_email_invalid_email_missing_host():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = []
    uc = UserController(dao=mockedDAO)

    with pytest.raises(ValueError):
        uc.get_user_by_email(email='jane.doe@email.')


@pytest.mark.unit
def test_get_user_by_email_db_failure():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.side_effect = Exception("Database error")
    uc = UserController(dao=mockedDAO)

    with pytest.raises(Exception, match= "Database error"):
        uc.get_user_by_email(email='jane.doe@email.com')
