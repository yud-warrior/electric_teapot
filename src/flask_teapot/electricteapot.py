from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)

from flask_teapot.db import get_db

bp = Blueprint('electricteapot', __name__)


@bp.route("/electricteapot")
def electricteapot():
    return render_template('electricteapot/electricteapot.html')


@bp.route("/time")
def time():
    data = {'time': datetime.utcnow().strftime('%F %T.%f')}
    return data
