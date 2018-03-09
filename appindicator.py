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
    '''Automated brighness controll GTK-appindicator.

    '''

    def __init__(self):
        self.ind = appindicator.Indicator.new(
            "Autodimmer",
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
        '''Starts GTK mainloop.

        '''
        print("running main")
        self.start_dimmer()
        Gtk.main()

    def start_dimmer(self):
        '''Starts automatic brightness controll.

        '''
        self.ind.set_icon(_curr_dir + 'dim_small.png')
        self.p = Process(target=dimmer.main)
        self.p.start()

    def stop_dimmer(self):
        '''Stops automatic brightness controll.

        '''
        if self.p.is_alive():
            self.ind.set_icon(_curr_dir + 'dim_grey_small.png')
            self.p.terminate()

    def toggle_stop(self, widget):
        '''Decides wether to start or stop automatic brightness controll.

        '''
        if self.p.is_alive():
            self.stop_dimmer()
        else:
            self.start_dimmer()
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

    def quit(self, widget):
        '''Terminates appindicator.
        '''
        self.stop_dimmer()
        Gtk.main_quit()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # to get ctrl+c working
    indicator = MyIndicator()
    indicator.main()
