import os

class Config:
    BASE_URL = os.getenv('TODO_URL','http://127.0.0.1:5000/api')
    TIMEOUT = 10
