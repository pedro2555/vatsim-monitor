from collections import defaultdict
from threading import Thread
from time import sleep

import vatsim

class Model:
    def __init__(self):
        self.listeners = defaultdict(set)

        self._loading = False
        self._icao = None
        self._pilots = []
        self.arrivals_listeners = set()
        self.departures_listeners = set()

        Thread(target=self.get_airport_info, daemon=True).start()

    def get_airport_info(self):
        while True:
            self.loading = True

            status = vatsim.status()
            sections = map(lambda x: x[1], status)
            _, _, clients, _, prefile = sections
            pilots = map(lambda x: x.split(':'), clients)
            pilots = filter(self._is_pilot, pilots)
            pilots = map(self._to_pilot, pilots)
            
            self.pilots = list(pilots)
            self.loading = False

            sleep(60)

    @property
    def loading(self):
        return self._loading

    @loading.setter
    def loading(self, value):
        self._loading = value
        self._notify('loading', value)

    @property
    def icao(self):
        return self._icao

    @icao.setter
    def icao(self, value):
        self._icao = value.upper()
        self._notify('arrivals', self.arrivals)
        self._notify('departures', self.departures)

    @property
    def pilots(self):
        return self._pilots

    @pilots.setter
    def pilots(self, value):
        self._pilots = value
        self._notify('arrivals', self.arrivals)
        self._notify('departures', self.departures)

    @property
    def departures(self):
        return list(filter(lambda x: x[2] == self.icao, self.pilots))

    @property
    def arrivals(self):
        return list(filter(lambda x: x[3] == self.icao, self.pilots))

    def on_loading_changed(self, callback):
        self.listeners['loading'].add(callback)

    def on_departures_changed(self, callback):
        self.listeners['departures'].add(callback)

    def on_arrivals_changed(self, callback):
        self.listeners['arrivals'].add(callback)

    def _notify(self, listener, args):
        for callback in self.listeners[listener]:
            callback(args)

    def _is_pilot(self, line):
        clienttype = line[3].upper()

        return clienttype == 'PILOT'

    def _to_pilot(self, line):
        callsign =    line[0]
        realname =    line[2]
        dep_airport = line[11].upper()
        arr_airport = line[13].upper()
        
        return [callsign, realname, dep_airport, arr_airport]

