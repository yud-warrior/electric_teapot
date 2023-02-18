from enum import Enum


from teapot.liquid import Liquid, Water
from teapot.heater import Heater


class TeapotState(Enum):
    ON = 1
    OFF = 2
    BOILED_UP = 3
    STOPPED = 4


class Teapot:

    INITIAL_TEMPERATURE = 15
    MAX_TEMPERATURE = 100
    TEMPERATURE_PRECISION = 2  # digits after floating point
    POWER = 2200
    VOLUME = 1.7

    def __init__(self):
        self.state: TeapotState = TeapotState.OFF
        self.rel_volume: float = 0.
        self.temperature: float = Teapot.INITIAL_TEMPERATURE
        self.liquid: Liquid = None
        self.heater: Heater = None

    def fill_with_water(self, rel_volume: float) -> None:
        if rel_volume < 0 or rel_volume > 1:
            raise ValueError
        self.rel_volume = rel_volume
        volume = rel_volume * Teapot.VOLUME
        self.liquid = Water(volume, Teapot.INITIAL_TEMPERATURE)

    def turn_on(self):
        self.state = TeapotState.ON
        self.heater = Heater(self.liquid, Teapot.POWER)
        self.heater.turn_on()
        self.work()

    def work(self):
        t = self.heater.temperature()
        while not self._turn_off_temperature(t):
            pass  # todo

    def _turn_off_temperature(temperature: float):
        rounded_t = round(temperature, Teapot.TEMPERATURE_PRECISION)
        return rounded_t >= Teapot.MAX_TEMPERATURE
