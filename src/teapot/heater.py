from datetime import datetime, timedelta

from teapot.liquid import Liquid


class Heater:

    def __init__(self, substance: Liquid, heat_power: float) -> None:
        self.substance: Liquid = substance
        self.power: float = heat_power
        self.on: bool = False
        self.started_at: datetime = None
        self.last_observed_at: datetime = None
        self.stopped_at: datetime = None

    def turn_on(self) -> None:
        self.started_at = datetime.utcnow()
        self.last_observed_at: datetime = self.started_at
        self.stopped_at: datetime = None

    def pause(self) -> None:
        pass

    def _update(self):
        current_time = datetime.utcnow()
        time_delta = current_time - self.last_observed_at
        self.last_observed_at = current_time
        self._update_substance_state(time_delta)

    def _update_substance_state(self, time_delta: timedelta) -> None:
        energy = self.power * time_delta.total_seconds()
        max_heat_energy = self._max_heating_energy_delta()
        if energy <= max_heat_energy:
            self._heating(energy)
        else:
            self._heating(max_heat_energy)
            energy -= max_heat_energy
            self._vaporating(max(energy, self._max_vaporating_energy_delta()))

    def _heating(self, energy_delta: float) -> None:
        sub = self.substance
        sub.temperature += energy_delta / (sub.heat_capacity * sub.mass)
    
    def _max_heating_energy_delta(self) -> float:
        sub = self.substance

        return sub.heat_capacity * sub.mass \
               * (sub.boiling_temperature - sub.temperature)

    def _vaporating(self, energy_delta: float) -> None:
        sub = self.substance
        sub.mass -= energy_delta / sub.vaporization_heat
    
    def _max_vaporating_energy_delta(self) -> float:
        sub = self.substance

        return sub.vaporization_heat * sub.mass
