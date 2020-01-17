class MainPresenter:
    def __init__(self, main_view, airports_service, list_presenter, item_presenter):
        self.view = main_view
        self.service = airports_service
        self.list_presenter = list_presenter
        self.item_presenter = item_presenter

        self._filter = ''
        self._airports = dict()

        airports_service.add_listener('loading', self.service_loading_changed)
        airports_service.add_listener('airports', self.service_airports_changed)
        main_view.on_txt_search_text_changed(self.txt_search_text_changed)

    def txt_search_text_changed(self, text):
        self._filter = text.upper()

        self._update_views()

    def service_loading_changed(self, loading):
        self.view.set_loading(loading)

    def service_airports_changed(self, airports):
        self._airports = airports

        self._update_views()

    def _update_views(self):
        if self.service.has_airport(self._filter):
            airport = self._airports[self._filter]

            self.item_presenter.show(airport)
        else:
            self.list_presenter.show(self._airports, self._filter)

class ListPresenter:
    def __init__(self, list_view):
        self.view = list_view

    def show(self, airports, _filter):
        self.view.show()

        _airports = filter(
            lambda v: isinstance(v.icao, str) and v.icao.startswith(_filter),
            airports.values()
        )
        self.view.set_airports(map(
            lambda p: [p.icao, str(len(p.arrivals)), str(len(p.departures)), str(len(p.controllers))],
            _airports
        ))

class ItemPresenter:
    def __init__(self, item_view):
        self.view = item_view

    def show(self, airport):
        self.view.show()

        def map_pilot(pilot):
            return [pilot.callsign, pilot.name, pilot.dep_icao, pilot.arr_icao]
        
        self.view.set_departures_text(f'Departures ({len(airport.departures)})')
        self.view.set_arrivals_text(f'Arrivals ({len(airport.arrivals)})')
        self.view.set_departures_list(map(map_pilot, airport.departures))
        self.view.set_arrivals_list(map(map_pilot, airport.arrivals))
