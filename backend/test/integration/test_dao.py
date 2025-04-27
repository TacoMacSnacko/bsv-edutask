import pymongo.errors
import pytest
import pymongo
import unittest.mock as mock
from unittest.mock import patch
from src.util.dao import DAO


@pytest.fixture
def entry():
    return { "username": "test name", "isActive": True, "notes": "asdasdasd" }

@pytest.fixture
def sut():
    dao = DAO(collection_name='test')
    yield dao

    dao.collection.drop()



def test_create_valid_entry(entry, sut):
    
    addedEntry = sut.create(entry)

    haveOriginalValues = set(entry).issubset(addedEntry)
    haveId = "_id" in addedEntry

    assert haveOriginalValues and haveId


def test_create_missing_required_value(entry, sut):

    del entry["isActive"]

    with pytest.raises(pymongo.errors.WriteError):
        addedEntry = sut.create(entry)
    

def test_create_wrong_type_bool(entry, sut):

    entry["isActive"] = "True"

    with pytest.raises(pymongo.errors.WriteError):
        addedEntry = sut.create(entry)


def test_create_wrong_type_string(entry, sut):

    entry["notes"] = True

    with pytest.raises(pymongo.errors.WriteError):
        addedEntry = sut.create(entry)


def test_create_duplicate_unique_value(entry, sut):
    
    with pytest.raises(pymongo.errors.WriteError):
        addedEntry1 = sut.create(entry)
        addedEntry2 = sut.create(entry)

