#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
import dimmer
import signal
from multiprocessing import Process
_curr_dir = "/".join(__file__.split("/")[:-1]) + "/"

'''
from
http://orkon.github.io/2014/08/31/extending-your-ubuntu-desktop-with-custom-indicator-applets-using-python3/
'''


class MyIndicator:
    def __init__(self):
        self.ind = appindicator.Indicator.new(
            "Autodimmer",
            "indicator-messages",
            appindicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()

        item_run = Gtk.MenuItem()
        item_run.set_label("Init")
        item_run.connect("activate", self.toggle_dimmer)
        self.item_run = item_run
        self.menu.append(item_run)

        item_learn = Gtk.MenuItem()
        item_learn.set_label("Start learning")
        item_learn.connect("activate", self.toggle_learning)
        self.item_learn = item_learn
        self.menu.append(item_learn)

        item_exit = Gtk.MenuItem()
        item_exit.set_label("Exit")
        item_exit.connect("activate", self.quit)
        self.item_exit = item_exit
        self.menu.append(item_exit)

        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def main(self):
        print("running main")
        self.start_dimmer()
        self.p_learn = Process(target=dimmer.dummy)
        Gtk.main()

    def start_dimmer(self):
        print("start dimmer")
        self.item_run.set_label("Stop")
        self.ind.set_icon(_curr_dir + 'icons/dim_small.png')
        self.p = Process(target=dimmer.main)
        self.p.start()

    def stop_dimmer(self):
        print("stop dimmer")
        self.item_run.set_label("Start")
        if self.p.is_alive():
            self.ind.set_icon(_curr_dir + 'icons/dim_grey_small.png')
            self.p.terminate()

    def start_learning(self,):
        print("learning dimmer")
        self.item_run.set_sensitive(False)
        self.item_exit.set_sensitive(False)
        self.stop_dimmer()
        self.ind.set_icon(_curr_dir + 'icons/learn_small.png')
        self.p_learn = Process(target=dimmer.aquire_data)
        self.p_learn.start()
        self.item_learn.set_label("Stop learning")

    def stop_learning(self,):
        print("stop learning")
        self.item_learn.set_sensitive(False)
        self.item_learn.set_label("learning...")
        if self.p_learn.is_alive():
            self.p_learn.terminate()
        self.p_learn = Process(target=dimmer.fit)
        self.p_learn.start()
        self.p_learn.join(timeout=120)
        self.p_learn.terminate()
        self.item_learn.set_label("Start learning")
        self.start_dimmer()
        self.item_exit.set_sensitive(True)
        self.item_learn.set_sensitive(True)
        self.item_run.set_sensitive(True)

    def toggle_learning(self, *args):
        if self.p_learn.is_alive():
            self.stop_learning()
        else:
            self.start_learning()

    def toggle_dimmer(self, widget):
        if self.p.is_alive():
            self.stop_dimmer()
        else:
            self.start_dimmer()
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

    def quit(self, widget):
        print("quit")
        self.stop_dimmer()
        Gtk.main_quit()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # to get ctrl+c working
    indicator = MyIndicator()
    indicator.main()
