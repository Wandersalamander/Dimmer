#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
import os
import dimmer
import signal
from multiprocessing import Process
_curr_dir = "/".join(__file__.split("/")[:-1]) + "/"
print(_curr_dir)
'''
from
http://orkon.github.io/2014/08/31/extending-your-ubuntu-desktop-with-custom-indicator-applets-using-python3/
'''


class MyIndicator:
    def __init__(self):
        self.ind = appindicator.Indicator.new(
            "Test",
            "indicator-messages",
            appindicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()

        item = Gtk.MenuItem()
        item.set_label("Start/Stop")
        item.connect("activate", self.toggle_stop)
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.quit)
        self.menu.append(item)

        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def main(self):
        print("running main")
        self.start_dimmer()
        Gtk.main()
        print()

    def start_dimmer(self):
        print("starting dimmer")
        self.ind.set_icon(_curr_dir + 'dim_small.png')
        self.p = Process(target=dimmer.main)
        self.p.start()
        print()

    def stop_dimmer(self):
        if self.p.is_alive():
            print("killed")
            self.ind.set_icon(_curr_dir + 'dim_grey_small.png')
            self.p.terminate()

    def toggle_stop(self, widget):
        print("process status:", self.p.is_alive())
        if self.p.is_alive():
            self.stop_dimmer()
        else:
            self.start_dimmer()
            print("started")
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        print()

    def quit(self, widget):
        print("quit")
        self.stop_dimmer()
        Gtk.main_quit()
        print()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indicator = MyIndicator()
    indicator.main()
