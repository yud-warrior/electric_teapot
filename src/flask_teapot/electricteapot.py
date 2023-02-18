from datetime import datetime
import asyncio

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)

from flask_teapot.db import get_db
from flask_teapot.teapot.teapot import Teapot, TeapotState, TeapotStateContext
from flask_teapot.crud import (
    insert_into_temperature_by_time, 
    insert_into_teapot_state,
    read_last_state,
)

bp = Blueprint('electricteapot', __name__)

task: asyncio.Task = None
teapot: Teapot = None


async def state_ctx_receiver(ctx: TeapotStateContext) -> None:
    await insert_into_temperature_by_time(ctx.temperature, ctx.time)
    await insert_into_teapot_state(ctx.state, ctx.time)

Teapot.STATE_CTX_RECEIVER = state_ctx_receiver


@bp.route("/electricteapot")
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


@bp.route("/turnon")
async def turnon():
    global teapot
    global task
    if teapot is None or teapot.state == TeapotState.OFF:
        teapot = Teapot()
        teapot.fill_with_water(1)
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
