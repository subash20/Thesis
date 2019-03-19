import json
import os


class Config(object):
    def __init__(self, filename="keycloak.json"):
        self.load_config(filename)

    def load_config(self, filename):
        filename = os.path.join(os.getcwd(), filename)
        with open(filename) as f:
            content = f.read()
        config = json.loads(content)
        self.realm = config["realm"]
        self.auth_server_url = config["auth-server-url"]
        self.ssl_required = config["ssl-required"]
        self.resource = config["resource"]
        self.secret = config["credentials"]["secret"]
