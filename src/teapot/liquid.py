from dataclasses import dataclass


@dataclass
class Liquid:
    volume: float # litres
    temperature: float # degree Celsius
    density: float # kq/ m**3
    heat_capacity: float # J/(kg * K)
    boiling_temperature: float # degree Celsius
    vaporization_heat: float # J/(kg * K)
    mass: float # kg


class Water(Liquid):

    DENSITY = 1.0
    HEAT_CAPACITY = 4180.6
    BOILING_TEMPERATURE = 100.
    VAPORIZATION_HEAT = 2.3e6

    def __init__(
            self,
            volume: float,
            temperature: float
    ) -> None:
        super().__init__(
            volume=volume,
            temperature=temperature,
            density=Water.DENSITY,
            heat_capacity=Water.HEAT_CAPACITY,
            boiling_temperature=Water.BOILING_TEMPERATURE,
            vaporization_heat=Water.VAPORIZATION_HEAT,
            mass=Water.DENSITY * volume
        )
        if volume < 0:
            raise ValueError
