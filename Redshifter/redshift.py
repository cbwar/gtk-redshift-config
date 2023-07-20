# -*- coding: utf-8 -*-

import os
from commentedconfigparser import CommentedConfigParser
import psutil
import time
import subprocess
from threading import Thread
from gi.repository import GObject


class RedshiftConfig:
    path = os.path.join(os.path.expanduser("~"), ".config", "redshift.conf")

    def __init__(self) -> None:
        self.read()

    def read(self):
        if not os.path.exists(self.path):
            raise "TODO: create file"

        self.config = CommentedConfigParser()
        self.config.read(self.path)

    def write(self):
        with open(self.path + "_temp", "w") as configfile:
            self.config.write(configfile)
        with open(self.path + "_temp", "r") as configfile:
            data = configfile.read().replace(" = ", "=")  # >:\
        with open(self.path + "_temp", "w") as configfile:
            configfile.write(data)
        os.rename(self.path + "_temp", self.path)
        print("file saved")

    def get_val(self, name, section="redshift"):
        return self.config[section][name]

    def set_val(self, name, new_value, section="redshift"):
        self.config[section][name] = new_value


class ProcessHandler(GObject.GObject):
    __gsignals__ = {
        "restarting": (GObject.SIGNAL_RUN_FIRST, None, ()),
        "restarted": (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def is_running(self):
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if "redshift" in proc.name().lower():
                    return proc.pid
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return None

    def start(self):
        p = subprocess.Popen(["redshift-gtk"])
        print("starting {}".format(p))

    def restart(self):
        pid = self.is_running()
        if pid:

            def restart_thread():
                print("restarting {}".format(pid))
                self.emit("restarting")
                p = psutil.Process(pid)
                p.terminate()
                time.sleep(5)
                self.start()
                print("pid {} restarted".format(pid))
                self.emit("restarted")

            thread = Thread(target=restart_thread)
            thread.start()

        else:
            print("not running")


if __name__ == "__main__":
    c = RedshiftConfig()
    print(c.get_val("temp-day"))
    print(c.get_val("temp-night"))
    c.set_val("temp-day", "5200")
    c.set_val("temp-night", "4800")
    c.write()

    p = ProcessHandler()
    print(p.is_running())
