from collections import defaultdict
from requests.exceptions import ConnectionError
from time import sleep
from threading import Thread

import vatsim

class AirportsService:
    def __init__(self):
        self._loading = False
        self._no_internet = False
        self._airports = dict()
        self._listeners = defaultdict(set)
        self._airports_listeners = set()

        Thread(target=self._pool_vatsim, daemon=True).start()

    def has_airport(self, icao):
        _icao = icao.upper()
        return len(_icao) == 4 and _icao in self.airports.keys()

    @property
    def loading(self):
        return self._loading

    @loading.setter
    def loading(self, value):
        self._loading = value

        for listener in self._listeners['loading']:
            listener(value)        

    @property
    def no_internet(self):
        return self._no_internet

    @no_internet.setter
    def no_internet(self, value):
        self._no_internet = value

        for listener in self._listeners['no_internet']:
            listener(value)

    @property
    def airports(self):
        return self._airports

    @airports.setter
    def airports(self, value):
        self._airports = value

        for listener in self._listeners['airports']:
            listener(value)

    def add_listener(self, prop, callback):
        self._listeners[prop].add(callback)

        value = getattr(self, prop)
        if value and len(value) > 0: callback(value)

    def _pool_vatsim(self, pool_seconds=60):
        while True:
            try:
                status = vatsim.status()
                parsed_sections = 1
                _, _, clients, _, prefile = map(lambda x: x[parsed_sections], status)
                clients = list(map(lambda x: x.split(':'), clients))
                pilots = filter(lambda x: x[3].upper() == 'PILOT', clients)

                airports = AirportDefaultDict()
                for pilot in pilots:
                    _pilot = Pilot(pilot[0], pilot[2], pilot[11], pilot[13])
                    airports[_pilot.dep_icao].departures.add(_pilot)
                    airports[_pilot.arr_icao].arrivals.add(_pilot)
            except ConnectionError:
                self.no_internet = True
            else:
                self.airports = airports
                self.no_internet = False

            self.loading = False
            sleep(60)
            self.loading = True

    def _notify(self):
        for listener in self._airports_listeners:
            listener(self.airports)

class AirportDefaultDict(dict):
    def __missing__(self, key):
        airport = Airport(key)

        self[key] = airport

        return airport

class Airport:
    def __init__(self, icao):
        self.icao = icao
        self.departures = set()
        self.arrivals = set()
        self.controllers = set()

    def __repr__(self):
        return f'Airport({self.icao})'

class Pilot:
    def __init__(self, callsign, name, dep_icao, arr_icao):
        self.callsign = callsign
        self.name = name
        self.dep_icao = dep_icao
        self.arr_icao = arr_icao

class Controller:
    def __init__(self, callsign, name):
        self.callsign = callsign
        self.name = name
