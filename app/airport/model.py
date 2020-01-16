from collections import defaultdict
from threading import Thread
from time import sleep

import vatsim

class Model:
    def __init__(self):
        self.loading = False
        self.pilots = []
        self.page = 'list'

        self._listeners = set()
        self._icao = ''

        def pool_airports():
            while True:
                self.loading = True
                self._notify()

                status = vatsim.status()
                sections = map(lambda x: x[1], status)
                _, _, clients, _, prefile = sections
                clients = list(clients)
                clients = map(lambda x: x.split(':'), clients)
                self.pilots = list(map(self._to_pilot, filter(self._is_pilot, clients)))
                
                self.loading = False
                self._notify()

                sleep(60)
        Thread(target=pool_airports, daemon=True).start()

    @property
    def icao(self):
        return self._icao

    @icao.setter
    def icao(self, value):
        self._icao = value.upper()

        if len(value) == 4:
            self.page = 'item'
        else:
            self.page = 'list'

        self._notify()

    @property
    def airports(self):
        arrivals = defaultdict(lambda: 0)
        departures = defaultdict(lambda: 0)
        controllers = defaultdict(lambda: 0)
        self._airports_icao = set()

        for pilot in self.pilots:
            departure = pilot[2]
            arrival = pilot[3]

            departures[departure] += 1
            arrivals[arrival] += 1

        _airports = set().union(arrivals.keys(), departures.keys(), controllers.keys())
        _airports = map(str, _airports)
        _airports = filter(lambda x: x != '', _airports)
        _airports = [
            airport for airport in _airports
            if self.icao == '' or airport.startswith(self.icao)]
        return [
            (
                airport,
                str(arrivals[airport]),
                str(departures[airport]),
                str(controllers[airport]))
            for airport in _airports
        ]

    @property
    def departures(self):
        return list(filter(lambda x: x[2] == self.icao, self.pilots))

    @property
    def arrivals(self):
        return list(filter(lambda x: x[3] == self.icao, self.pilots))

    def add_listener(self, listener):
        self._listeners.add(listener)

    def _notify(self):
        for listener in self._listeners:
            listener(self)

    def _is_pilot(self, line):
        clienttype = line[3].upper()

        return clienttype == 'PILOT'

    def _to_pilot(self, line):
        callsign =    line[0]
        realname =    line[2]
        dep_airport = line[11].upper()
        arr_airport = line[13].upper()
        
        return [callsign, realname, dep_airport, arr_airport]

