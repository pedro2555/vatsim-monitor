from gi.repository import Gtk, GLib

class MainView:
    def __init__(self, builder):
        self._window = builder.get_object('airport_window')
        self._txt_search_text_change_listeners = set()

        builder.connect_signals(self)

    def show(self):
        self._window.show_all()

    def on_txt_search_text_changed(self, callback):
        self._txt_search_text_change_listeners.add(callback)

    def on_txt_search_changed(self, widget, data=None):
        text = widget.get_text()

        for listener in self._txt_search_text_change_listeners:
            listener(text)

    def on_airport_window_destroy(self, widget, data=None):
        Gtk.main_quit()

class ListView:
    def __init__(self, builder):
        self.stack =          builder.get_object('stack')
        self.airports_store = builder.get_object('airports_store')

    def set_airports(self, value):
        GLib.idle_add(_update_list_store, self.airports_store, value)

    def show(self):
        GLib.idle_add(self.stack.set_visible_child_name, 'list')

class ItemView:
    def __init__(self, builder):
        self.stack =          builder.get_object('stack')
        self.arrivals =       builder.get_object('arrivals_store')
        self.departures =     builder.get_object('departures_store')
        self.txt_arrivals =   builder.get_object('txt_arrivals')
        self.txt_departures = builder.get_object('txt_departures')

    def show(self):
        GLib.idle_add(self.stack.set_visible_child_name, 'item')

    def set_departures_text(self, text):
        GLib.idle_add(self.txt_departures.set_text, text)

    def set_arrivals_text(self, text):
        GLib.idle_add(self.txt_arrivals.set_text, text)

    def set_departures_list(self, departures):
        GLib.idle_add(_update_list_store, self.departures, departures)

    def set_arrivals_list(self, arrivals):
        GLib.idle_add(_update_list_store, self.arrivals, arrivals)
        
def _update_list_store(list_store, items):
    list_store.clear()
    for item in items:
        list_store.append(item)