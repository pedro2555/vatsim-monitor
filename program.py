#!/usr/bin/python3
from app import airport

if __name__ == '__main__':
    model = airport.Model()
    presenter = airport.Presenter(model)

    presenter.run()
