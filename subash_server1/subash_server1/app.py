from flask import Blueprint, Flask
from flask_login import LoginManager, login_required

from flask_keycloak import Keycloak

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisIsRequired-SomeStrongSecretKey"
# mandatory config for keycloak
app.config["KEYCLOAK_REDIRECT_URL"] = "index"
#app.config["KEYCLOAK_REDIRECT_URL"] = "logout"
keycloak = Keycloak(app)

