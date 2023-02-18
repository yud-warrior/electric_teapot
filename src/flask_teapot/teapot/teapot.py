from enum import Enum
from dataclasses import dataclass
import asyncio
from datetime import datetime

from flask_teapot.teapot.liquid import Liquid, Water
from flask_teapot.teapot.heater import Heater


class TeapotState(Enum):
    ON = 1
    OFF = 2
    BOILED_UP = 3
    STOPPED = 4


@dataclass
class TeapotStateContext:
    state: TeapotState
    temperature: float
    time: str


class Teapot:

    INITIAL_TEMPERATURE = 15
    MAX_TEMPERATURE = 100
    TEMPERATURE_PRECISION = 2  # digits after floating point
    POWER = 10000  # 2200
    VOLUME = 1.7
    SENSOR_TIMEDELTA = 1  # seconds
    STATE_CTX_RECEIVER = None
    CHANGED_STATE_CTX_RECEIVER = None

    def __init__(self):
        self.state: TeapotState = TeapotState.OFF
        self.rel_volume: float = 0.
        self.temperature: float = Teapot.INITIAL_TEMPERATURE
        self.liquid: Liquid = None
        self.heater: Heater = None
        self.state_ctx_receiver: asyncio.coroutine = Teapot.STATE_CTX_RECEIVER
        self.changed_state_ctx_receiver: asyncio.coroutine = \
            Teapot.CHANGED_STATE_CTX_RECEIVER

    def fill_with_water(self, rel_volume: float) -> None:
        if rel_volume < 0 or rel_volume > 1:
            raise ValueError
        self.rel_volume = rel_volume
        volume = rel_volume * Teapot.VOLUME
        self.liquid = Water(volume, Teapot.INITIAL_TEMPERATURE)

    def turn_on(self) -> asyncio.Task:
        self.state = TeapotState.ON
        self.heater = Heater(self.liquid, Teapot.POWER)
        self.heater.turn_on()
        loop = asyncio.get_event_loop()
        time = datetime.utcnow()
        ctx = TeapotStateContext(
            self.state,
            self.temperature,
            time.strftime('%F %T.%f')
        )
        loop.create_task(self.send_changed_state_ctx(ctx))
        task = loop.create_task(self.work())
        return task

    async def work(self) -> None:
        t = self.heater.temperature()
        while not self._turn_off_temperature(t):
            try:
                asyncio.create_task(self.send_ctx(t))
                await asyncio.sleep(Teapot.SENSOR_TIMEDELTA)
                t = self.heater.temperature()
            except asyncio.CancelledError:
                self.state = TeapotState.OFF
                self.heater.turn_off()
                await self.send_changed_state_ctx(t)
                await self.send_ctx(t)
                return

        self.state = TeapotState.BOILED_UP
        await self.send_changed_state_ctx(t)
        await self.send_ctx(t)

        self.heater.turn_off()
        await asyncio.sleep(0.1)

        self.state = TeapotState.OFF
        await self.send_changed_state_ctx(t)
        await self.send_ctx(t)

    async def send_ctx(self, temperature: float) -> None:
        if self.state == TeapotState.OFF:
            time = self.heater.stopped_at
        else:
            time = self.heater.last_observed_at
        str_time = time.strftime('%F %T.%f')
        ctx = TeapotStateContext(self.state, temperature, str_time)
        await self.state_ctx_receiver(ctx)

    async def send_changed_state_ctx(self, temperature: float) -> None:
        if self.state == TeapotState.OFF:
            time = self.heater.stopped_at
        else:
            time = self.heater.last_observed_at
        str_time = time.strftime('%F %T.%f')
        ctx = TeapotStateContext(self.state, temperature, str_time)
        await self.changed_state_ctx_receiver(ctx)

    def _turn_off_temperature(self, temperature: float) -> bool:
        rounded_t = round(temperature, Teapot.TEMPERATURE_PRECISION)
        return rounded_t >= Teapot.MAX_TEMPERATURE
