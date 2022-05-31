import os

import yaml


class Settings:
    def __init__(self):
        self.path = self.config_path()
        with open(self.path, 'r') as conf:
            yaml_file = yaml.safe_load(conf)
            self.db_name = yaml_file["db_name"]
            self.db_username = yaml_file["db_username"]
            self.db_host = yaml_file["db_host"]
            self.db_port = yaml_file["db_port"]
            self.db_password = yaml_file["db_password"]
            self.secret_key = yaml_file["secret_key"]
        self.default = self.default_config()

    def default_config(self):
        default = {
            "db_name": self.db_name,
            "db_username": self.db_username,
            "db_host": self.db_host,
            "db_port": self.db_port,
            "db_password": self.db_password,
            "secret_key": self.secret_key
        }
        return default

    @staticmethod
    def config_path():
        raw_path = os.path.dirname(__file__)
        raw_path = raw_path.split('/')
        raw_path.pop(-1)
        raw_path.append('config.yml')
        path = '/'.join(raw_path)
        return path

    def config_for_tests(self):
        with open(self.path, 'w') as file:
            yaml.dump({
                "db_name": "test_messanger",
                "db_username": "wood",
                "db_password": "123",
                "db_port": 5432,
                "db_host": "localhost",
                "secret_key": "secret_key"
            }, file)
        self.db_name = "test_messanger"
        self.db_username = "wood"
        self.db_password = "123"
        self.db_port = 5432
        self.db_host = "localhost"
        self.secret_key = "secret_key"

    def reset_default_config(self):
        with open(self.path, 'w') as file:
            yaml.dump(self.default, file)
            file.flush()
