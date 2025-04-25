import pytest
import unittest.mock as mock
from unittest.mock import patch
from src.util.dao import DAO


@pytest.fixture
def entry():
    return { "username": "test name", "isActive": True, "notes"   : "asdasdasd" }


def test_create_valid_entry(entry):

    dao = DAO(collection_name='test')
    addedEntry = dao.create(entry)
    dao.collection.drop()

    assert set(entry).issubset(addedEntry) and "_id" in addedEntry


def test_create_missing_required_value(entry):

    del entry["isActive"]

    dao = DAO(collection_name='test')

    with pytest.raises(Exception):
        addedEntry = dao.create(entry)
        dao.collection.drop()


def test_create_missing_non_required_value(entry):

    del entry["notes"]

    dao = DAO(collection_name='test')
    addedEntry = dao.create(entry)
    dao.collection.drop()

    assert set(entry).issubset(addedEntry) and "_id" in addedEntry


def test_create_wrong_type(entry):

    entry["isActive"] = "True"

    dao = DAO(collection_name='test')

    with pytest.raises(Exception):
        addedEntry = dao.create(entry)
        dao.collection.drop()


def test_create_duplicate_unique_value(entry):

    dao = DAO(collection_name='test')

    with pytest.raises(Exception):
        addedEntry1 = dao.create(entry)
        addedEntry2 = dao.create(entry)
        dao.collection.drop()

