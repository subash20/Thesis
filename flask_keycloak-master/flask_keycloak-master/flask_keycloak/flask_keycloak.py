
import base64
import json

from flask import Blueprint, redirect, request, session, url_for, flash
from flask_login import logout_user, UserMixin, login_user, login_required, LoginManager
import requests

from flask_keycloak.config import Config


KEYCLOAK_REDIRECT_URL = None
keycloak = Blueprint("keycloak", __name__)


class Keycloak(object):
    def __init__(self, app):
        global KEYCLOAK_REDIRECT_URL

        app.register_blueprint(keycloak)
        login_manager = LoginManager(app)

        login_manager.user_loader(user_loader) # is used to reload user object from USer ID stored in session.
        login_manager.request_loader(request_loader)# login user without cookies
        login_manager.unauthorized_handler(unauthorized_handler)
        KEYCLOAK_REDIRECT_URL = app.config.get("KEYCLOAK_REDIRECT_URL")


class KeycloakConfig(Config):
    def __init__(self):
        super(KeycloakConfig, self).__init__()

        self._token_url = None
        self._auth_url = None
        self._logout_url = None
        self._userinfo_url = None

    @property
    def token_url(self):
        """
        /realms/{realm-name}/protocol/openid-connect/token

        This is the URL endpoint for obtaining a temporary code in the
        Authorization Code Flow or for obtaining tokens via the Implicit Flow,
        Direct Grants, or Client Grants.
        """
        print ("**********")
        return "{url}/realms/{realm_name}/protocol/openid-connect/token".format(
            url=self.auth_server_url, realm_name=self.realm)

    @property
    def auth_url(self):
        """
        /realms/{realm-name}/protocol/openid-connect/auth

        This is the URL endpoint for the Authorization Code Flow to turn a
        temporary code into a token.
        """
        return "{url}/realms/{realm_name}/protocol/openid-connect/auth".format(
            url=self.auth_server_url, realm_name=self.realm)

    @property
    def logout_url(self):
        """
        /realms/{realm-name}/protocol/openid-connect/logout

        This is the URL endpoint for performing logouts.
        """
        return "{url}/realms/{realm_name}/protocol/openid-connect/logout".format(
            url=self.auth_server_url, realm_name=self.realm)

    @property
    def userinfo_url(self):
        """
        /realms/{realm-name}/protocol/openid-connect/userinfo

        This is the URL endpoint for the User Info service described in the OIDC specification.
        """
        return "{url}/realms/{realm_name}/protocol/openid-connect/userinfo".format(
            url=self.auth_server_url, realm_name=self.realm)

def b64tojson(string):
    """Convert base64 string to dict object

    - Pad stripped or incorrectly formatted base64 string
    - Decode base64 string
    - Deserialize JSON string to dict object

    :param b64_string: base64 string
    :return: dict object
    """
    restore_b64 = lambda string: string + '=' * (-len(string) % 4)
    return json.loads(base64.b64decode(restore_b64(string)).decode("utf-8"))

def parse_user_roles(payload):
    """Parse user roles from access_token payload

    :param payload: JSON object
    :return: list of user roles
    """
    #: TODO handle parsing user roles and give proper error or info message
    resource_access = payload["resource_access"]
    if resource_access.get(keycloak_config.resource):
        return resource_access[keycloak_config.resource]["roles"]
    return resource_access["account"]["roles"]


# Flask-Login related
class User(UserMixin):
    pass


def user_loader(email):
    user_info = session.get("user_info")
    if not user_info:
        return

    user = User()
    user.id = user_info["email"]
    return user


def request_loader(request):
    user_info = session.get("user_info")
    if not user_info:
        return

    user = User()
    user.id = user_info["email"]
    user.is_authenticated = True
    return user


def unauthorized_handler():
    return redirect(keycloak_auth_url())


# KeycloakConfig related
keycloak_config = KeycloakConfig()


@keycloak.route("/oauth2_callback")
def oauth2_callback():
    code = request.args.get("code")
    headers = {"content-type": "application/x-www-form-urlencoded"}
    redirect_uri = url_for(".oauth2_callback", _external=True)
    data = "client_id={}&grant_type=authorization_code&code={}&redirect_uri={}&client_secret={}".format(
        keycloak_config.resource, code, redirect_uri, keycloak_config.secret)

    r = requests.post(keycloak_config.token_url, data=data, headers=headers)
    if r.status_code == 200:
        restore_bs64_eq = lambda string: string + '=' * (-len(string) % 4)
      #  print ("**************")
        t = json.loads(r.text)

        access_token = t["access_token"]
        access_token_ = access_token.split(".")
        header = b64tojson(access_token_[0])
        payload = b64tojson(access_token_[1])
        user_roles = parse_user_roles(payload)
        #: TODO *** UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa9 in position 7: invalid start byte
        # signature = b64tojson(access_token_[2])
        expires_in = t["expires_in"]
        refresh_expires_in = t["refresh_expires_in"]
        refresh_token = t["refresh_token"]
        token_type = t["token_type"]
        # id_token = t["id_token"]
        not_before_policy = t["not-before-policy"]
        session_state = t["session_state"]

        # get user details
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer {}".format(access_token)
        }
        user_data = requests.get(keycloak_config.userinfo_url, headers=headers)
        user_info = json.loads(user_data.text)

        user = User()
        user.id = user_info.get("email")
        login_user(user)
        session["access_token"] = access_token
        session["user_info"] = user_info
        session["user_roles"] = user_roles

        flash("Login Successful")
    return redirect(url_for(KEYCLOAK_REDIRECT_URL))


@keycloak.route("/logout/")
@login_required
def logout():
    logout_user()
    session.clear()

    # Redirect to logout itself so that Flask-Login would redirect to keycloak login page
    redirect_url = "{}?redirect_uri={}".format(
        keycloak_config.logout_url, url_for(".logout", _external=True))
    return redirect(redirect_url)


def keycloak_auth_url():
    redirect_uri = url_for("keycloak.oauth2_callback", _external=True)
    return "{}?client_id={}&redirect_uri={}&response_type=code".format(
        keycloak_config.auth_url, keycloak_config.resource, redirect_uri)
