import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

class Presenter:
    def __init__(self, model):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('gui/airport/view.glade')
        self.builder.connect_signals(self)

        self.main_window = self.builder.get_object('airport_window')
        self.main_window.show_all()

        self.spinner = self.builder.get_object('spinner')
        self.arrivals = self.builder.get_object('arrivals_store')
        self.departures = self.builder.get_object('departures_store')

        self.model = model
        model.on_arrivals_changed(self._update_arrivals)
        model.on_departures_changed(self._update_departures)

    def run(self):
        Gtk.main()

    def on_airport_window_destroy(self, widget, data=None):
        Gtk.main_quit()

    def on_txt_search_changed(self, widget, data=None):
        text = widget.get_text()

        if len(text) != 4:
            return

        self.spinner.start()
        self.model.set_icao(text)

    def _update_arrivals(self, arrivals):
        self._update_list_store(self.arrivals, arrivals)

    def _update_departures(self, departures):
        self._update_list_store(self.departures, departures)

    def _update_list_store(self, list_store, items):
        list_store.clear()
        for item in items:
            list_store.append(item)

        self.spinner.stop()