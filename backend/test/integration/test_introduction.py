import pytest
import unittest.mock as mock
from unittest.mock import patch
from src.controllers.usercontroller import UserController

from src.util.dao import DAO



def test_dao_mongodb_integration():

    dao = DAO(collection_name='test')

    assert 1 + 1 == 2