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
        self.last_observed_at: datetime = None
        self.stopped_at: datetime = None

    def pause(self) -> None:
        pass
