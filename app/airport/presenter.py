import gi
gi.require_version('Gtk', '3.0')

from gi.repository import GLib, Gtk, GObject

class Presenter:
    def __init__(self, model):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('app/airport.glade')
        self.builder.connect_signals(self)

        self.main_window = self.builder.get_object('airport_window')
        self.main_window.show_all()

        self.spinner = self.builder.get_object('spinner')
        self.arrivals = self.builder.get_object('arrivals_store')
        self.departures = self.builder.get_object('departures_store')
        self.txt_arrivals = self.builder.get_object('txt_arrivals')
        self.txt_departures = self.builder.get_object('txt_departures')

        self.model = model
        model.add_listener(self._on_model_changed)

        self.search_text = ''

    def run(self):
        Gtk.main()

    def on_airport_window_destroy(self, widget, data=None):
        Gtk.main_quit()

    def on_txt_search_changed(self, widget, data=None):
        self.search_text = widget.get_text()
        self._search_changed()

    def _search_changed(self):
        if len(self.search_text) != 4:
            return

        self.model.icao = self.search_text

    def _on_model_changed(self, model):
        self._update_loading(model.loading)
        self._update_arrivals(model.arrivals)
        self._update_departures(model.departures)

    def _update_loading(self, loading):
        if loading:
            GLib.idle_add(self.spinner.start)
        else:
            GLib.idle_add(self.spinner.stop)

    def _update_arrivals(self, arrivals):
        GLib.idle_add(lambda: self.txt_arrivals.set_text(f'Arrivals ({len(arrivals)})'))
        GLib.idle_add(self._update_list_store, self.arrivals, arrivals)

    def _update_departures(self, departures):
        GLib.idle_add(lambda: self.txt_departures.set_text(f'Departures ({len(departures)})'))
        GLib.idle_add(self._update_list_store, self.departures, departures)

    def _update_list_store(self, list_store, items):
        list_store.clear()
        for item in items:
            list_store.append(item)