import os
import sys
import time

import grpc
import pytest

from server.proto_api.server_proto_pb2_grpc import MessangerStub
from tests.config import Settings
from tests.orm import Orm
from tests.server_command import terminate_server
# from proto_api.server_proto_pb2_grpc import MessangerStub
print(sys.path)

config = Settings()


@pytest.fixture(scope='session')
def server_start():
    config.config_for_tests()
    os.popen('sh server_start.sh')
    time.sleep(0.4)
    yield
    config.reset_default_config()
    terminate_server()


@pytest.fixture(scope='function')
def orm():
    orm = Orm(config)
    orm.create_test_clients()
    yield orm
    orm.clearing_database()


@pytest.fixture(scope='function')
def send_message():
    with grpc.insecure_channel('localhost:5001') as channel:
        stub = MessangerStub(channel)
        yield stub
