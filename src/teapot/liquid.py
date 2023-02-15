from dataclasses import dataclass


@dataclass
class Liquid:
    volume: float # litres
    density: float # kq/ m**3
    heat_capacity: float # J/(kg * K)
    boiling_temperature: float # Celsius degree
    vaporization_heat: float # J/(kg * K)


class Water(Liquid):

    def __init__(
            self,
            volume: float
    ) -> None:
        super.__init__(
            volume=volume,
            density=1.0,
            heat_capacity=4180.6,
            boiling_temperature=100,
            vaporization_heat=2.3e6
        )
        if volume < 0:
            raise ValueError
        self.mass = self.density * self.volume # kg