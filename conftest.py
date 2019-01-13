import json

import pytest

from db.mongo import MongoClient
from scripts.parse_log import ParseGamesLog


@pytest.fixture
def collection():
    return MongoClient().collection


@pytest.fixture(autouse=True)
def games_db_drop(collection):
    collection.drop()


@pytest.fixture
def file_response_json():
    with open('response.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def populate_db():
    ParseGamesLog().parse_log()
