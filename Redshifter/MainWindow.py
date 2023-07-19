# -*- coding: utf-8 -*-

import gi

gi.require_version("GMenu", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk, GMenu
from Redshifter.redshift import RedshiftConfig, ProcessHandler
import gettext
from Redshifter.form import validate_color_temp
from Redshifter import config

gettext.bindtextdomain(config.GETTEXT_PACKAGE, config.localedir)
gettext.textdomain(config.GETTEXT_PACKAGE)

_ = gettext.gettext


class MainWindow(object):
    def __init__(self):
        Gtk.Window.set_default_icon_name("redshifter")
        self.tree = Gtk.Builder()
        self.tree.set_translation_domain(config.GETTEXT_PACKAGE)
        self.tree.add_from_file("./data/redshifter.ui")
        self.tree.connect_signals(self)
        self.main_window = self.tree.get_object("mainwindow")
        self.init()

    def run(self):
        self.tree.get_object("mainwindow").show_all()
        Gtk.main()

    def init(self):
        self.init_fields()
        self.init_restart_btn()


    def init_fields(self):
        config = RedshiftConfig()
        self.tree.get_object("field_day_temp").set_text(config.get_val("temp-day"))
        self.tree.get_object("field_night_temp").set_text(config.get_val("temp-night"))

    def init_restart_btn(self):
        p = ProcessHandler()
        if p.is_running() is None:
            self.tree.get_object("btn_restart").set_sensitive(False)
        else:
            self.tree.get_object("btn_restart").set_sensitive(True)

    def on_save_clicked(self, button):
        config = RedshiftConfig()
        temp = self.tree.get_object("field_day_temp").get_text()
        temp = validate_color_temp(temp)
        config.set_val("temp-day", temp)
        temp = self.tree.get_object("field_night_temp").get_text()
        temp = validate_color_temp(temp)
        config.set_val("temp-night", temp)
        config.write()
        self.init()

    def on_restart_clicked(self, button):
        self.on_save_clicked(button)
        p = ProcessHandler()

        def restarting(arg):
            self.tree.get_object("btn_restart").set_sensitive(False)

        def restarted(arg):
            self.tree.get_object("btn_restart").set_sensitive(True)

        p.connect("restarting", restarting)
        p.connect("restarted", restarted)
        p.restart()

    def on_close_clicked(self, button):
        self.quit()

    def on_delete_event(self, widget, event):
        self.quit()

    def quit(self):
        Gtk.main_quit()


def main():
    app = MainWindow()
    app.run()
