#!/usr/bin/env python3
from subprocess import Popen, PIPE
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import GLib as glib
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

# Subroutines
def change_status(__panel__, __change__, __file__):
    __panel__.set_icon(gtk.STOCK_REFRESH)
    __panel__.set_label(' Updating ', '')
    with open(__file__, "w") as __status__:
        __status__.write(__change__)
    __status__.close()

def update_panel(__panel__):
    if (update_status(__STATUSFILE__) == "0"):
        __panel__.set_icon(gtk.STOCK_REFRESH)
        __panel__.set_label(' No Security', '')

def update_status(__file__):
    with open(__file__, "r") as __status__:
        __current__ = __status__.read()
    __status__.close()
    return __current__.rstrip()

# Constants
__STATUSFILE__ = "status"
__APPINDICATORID__ = "Correctness Desktop Security"

# Global variables
__currentstatus__ = update_status(__STATUSFILE__)

# Application
__app__ = appindicator.Indicator.new(__APPINDICATORID__, 
   gtk.STOCK_REFRESH, appindicator.IndicatorCategory.SYSTEM_SERVICES)
__app__.set_status(appindicator.IndicatorStatus.ACTIVE)
__app__.set_label(' Updating','')

# Menu
__menu__ = gtk.Menu()
__app__.set_menu(__menu__)

# Menu options
__exit__ = gtk.MenuItem("Exit")
__menu__.append(__exit__)
__exit__.connect("activate", quit)
__exit__.show_all()

# Run time
glib.timeout_add(1000, update_panel, __app__)
gtk.main()

