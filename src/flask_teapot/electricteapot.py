from datetime import datetime
import asyncio

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request, session,
    url_for,
    json
)

from flask_teapot.teapot.teapot import Teapot, TeapotState, TeapotStateContext
import flask_teapot.teapot.config as teapot_config
from flask_teapot.crud import (
    insert_into_temperature_by_time,
    insert_into_teapot_state,
    read_last_state,
    read_last_temperature,
)

bp = Blueprint('electricteapot', __name__)


async def state_ctx_receiver(ctx: TeapotStateContext) -> None:
    await insert_into_temperature_by_time(ctx.temperature, ctx.time)


async def changed_state_ctx_receiver(ctx: TeapotStateContext) -> None:
    await insert_into_teapot_state(ctx.state, ctx.time)


def setup_teapot():
    Teapot.INITIAL_TEMPERATURE = teapot_config.INITIAL_TEMPERATURE
    Teapot.MAX_TEMPERATURE = teapot_config.MAX_TEMPERATURE
    Teapot.TEMPERATURE_PRECISION = teapot_config.TEMPERATURE_PRECISION
    Teapot.POWER = teapot_config.POWER
    Teapot.VOLUME = teapot_config.VOLUME
    Teapot.SENSOR_TIMEDELTA = teapot_config.SENSOR_TIMEDELTA
    Teapot.STATE_CTX_RECEIVER = state_ctx_receiver
    Teapot.CHANGED_STATE_CTX_RECEIVER = changed_state_ctx_receiver


setup_teapot()
task: asyncio.Task = None
teapot: Teapot = None
water_rel_volume = 1


@bp.route("/")
def electricteapot():
    return render_template('electricteapot/electricteapot.html')


@bp.route("/time")
def time():
    data = {'time': datetime.utcnow().strftime('%F %T.%f')}
    return data


@bp.route("/state")
async def state():
    state = await read_last_state()
    if state is None:
        return {'state': 'no state'}
    return {'state': state.name}


@bp.route("/relvolume")
def relvolume():
    global water_rel_volume
    return {'relvolume': water_rel_volume}


@bp.route("/temperature")
async def temperature():
    temperature = await read_last_temperature()
    if temperature is None:
        return {'temperature': Teapot.INITIAL_TEMPERATURE}
    return {'temperature': temperature}


@bp.route("/turnon")
async def turnon():
    global teapot
    global task
    global water_rel_volume
    if teapot is None or teapot.state == TeapotState.OFF:
        teapot = Teapot()
    teapot.fill_with_water(water_rel_volume)
    if task is None:
        task = teapot.turn_on()
        await task
        teapot.state = TeapotState.OFF
        task = None
        return {'message': ''}
    return {'message': 'teapot has already turned on'}


@bp.route("/turnoff")
def turnoff():
    global teapot
    global task
    if task is None:
        return {'message': 'teapot has already turned off'}
    if task.done():
        task = None
        return {'message': 'teapot has already turned off'}
    task.cancel()
    return {'message': ''}


@bp.route("/getrelvolume", methods=['GET', 'POST'])
def getrelvolume():
    if request.method == 'POST':
        global water_rel_volume
        val = float(request.form['relvolume'])
        if 0 < val <= 1:
            water_rel_volume = val
        return render_template('electricteapot/electricteapot.html')
    else:
        return render_template('electricteapot/electricteapot.html')
