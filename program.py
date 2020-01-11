#!/usr/bin/python3
from gui import airport

if __name__ == '__main__':
    model = airport.Model()
    presenter = airport.Presenter(model)

    presenter.run()
