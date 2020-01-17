#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from app.airports import *

builder = Gtk.Builder()
builder.add_from_file('app/airport.glade')

main_view = MainView(builder)
list_view = ListView(builder)
item_view = ItemView(builder)

airports_service = AirportsService()

list_presenter = ListPresenter(list_view)
item_presenter = ItemPresenter(item_view)
main_presenter = MainPresenter(main_view, airports_service, list_presenter, item_presenter)

if __name__ == '__main__':
    main_presenter.view.show()
    Gtk.main()
