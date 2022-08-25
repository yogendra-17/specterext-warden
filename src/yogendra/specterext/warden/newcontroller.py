from flask import render_template, redirect, url_for
from .service import WardenService



warden_endpoint = WardenService.blueprints["default"]


# extension must have a view called index
# full path becomes : http://127.0.0.1:25441/svc/warden/default/
@warden_endpoint.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for('warden_routes_endpoint.warden_page'))
