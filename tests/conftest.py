import os
import time

import grpc
import pytest

from config import Settings
from orm import Orm
from server_command import terminate_server
from server_proto_pb2_grpc import GreeterStub

config = Settings()


@pytest.fixture(scope='session')
def server_start():
    config.config_for_tests()
    os.popen('sh server_start.sh')
    time.sleep(0.5)
    yield
    config.reset_default_config()
    terminate_server()


@pytest.fixture(scope='function')
def orm():
    orm = Orm(config)
    orm.test_client_add()
    yield orm
    orm.delete_test_client()


@pytest.fixture(scope='function')
def send_message():
    with grpc.insecure_channel('localhost:5000') as channel:
        stub = GreeterStub(channel)
        yield stub
