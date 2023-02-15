from enum import Enum


from teapot.liquid import Liquid


class TeapotState(Enum):
    ON = 1
    OFF = 2
    BOILED_UP = 3
    STOPPED = 4


class Teapot:

    INITIAL_TEMPERATURE = 15
    MAX_TEMPERATURE = 100

    def __init__(self):
        self.state: TeapotState = TeapotState.OFF
        self.rel_volume: float = 0.
        self.temperature: float = Teapot.INITIAL_TEMPERATURE
        self.liquid: Liquid = None