import pytest
import logging
from test_client import Todoclient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test.log'),
        logging.StreamHandler()
    ]
)

@pytest.fixture(scope='session')
def todo_client():
    client = Todoclient()
    yield client
    client.session.close()

@pytest.fixture(scope='function')
def clean_todos(todo_client):
    resp = todo_client.get()
    if resp.status_code == 200:
        todos = resp.json()
        for todo in todos:
            todo_client.delete(todo['id'])
    yield