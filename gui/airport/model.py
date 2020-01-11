from collections import defaultdict

import vatsim

class Model:
    def __init__(self):
        self.listeners = defaultdict(set)

        self.icao = None
        self.arrivals_listeners = set()
        self.departures_listeners = set()

    def set_icao(self, icao):
        self.icao = icao.upper()

        status = vatsim.status()
        sections = map(lambda x: x[1], status)
        _, _, clients, _, prefile = sections
        clients = map(lambda x: x.split(':'), clients)
        clients = list(clients)

        departures = filter(self._is_departure, clients)
        self._notify('departures', map(self._to_departure, departures))

        arrivals = filter(self._is_arrival, clients)
        self._notify('arrivals', map(self._to_arrival, arrivals))

    def on_arrivals_changed(self, callback):
        self.listeners['arrivals'].add(callback)

    def on_departures_changed(self, callback):
        self.listeners['departures'].add(callback)

    def _notify(self, listener, args):
        for callback in self.listeners[listener]:
            callback(args)

    def _is_arrival(self, line):
        clienttype =   line[3].upper()
        arrival_icao = line[13].upper()

        return clienttype == 'PILOT' and arrival_icao == self.icao

    def _is_departure(self, line):
        clienttype =     line[3].upper()
        departure_icao = line[11].upper()

        return clienttype == 'PILOT' and departure_icao == self.icao

    def _to_arrival(self, line):
        callsign =       line[0]
        realname =       line[2]
        departure_icao = line[11].upper()
        
        return [callsign, realname, departure_icao]

    def _to_departure(self, line):
        callsign =     line[0]
        realname =     line[2]
        arrival_icao = line[13].upper()
        
        return [callsign, realname, arrival_icao]

