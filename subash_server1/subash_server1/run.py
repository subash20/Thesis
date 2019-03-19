from flask import render_template, session
from flask_login import login_required
from flask import send_file
from flask_keycloak import Keycloak

from functools import wraps
import os
from app import app


# This does all the magic of SSO
#app.register_blueprint(Keycloak)


def requires_roles(role):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # if get_current_user_role() not in roles:
            if role not in session["user_roles"]:
                return "User does not have {} role".format(role)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@app.route("/")
@login_required
def index():
    """ get role from keycloak, all manipulation done here"""

    return render_template("index.html", role="cannot_download")

@app.route("/protected/")
@login_required
def protected():
    return "protected page"

@app.route("/about/")
@login_required
def about():
    return "about page"

@app.route("/view/")
@login_required
def view():
    return "some view content"

@app.route("/download/<filename>")
@requires_roles('can_download')
@login_required
def download(filename):
    return send_file(os.path.join("images", filename), as_attachment=True)

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
