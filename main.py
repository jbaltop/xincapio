# Copyright (C) 2019 Hajun Park
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# standard library
import json
import logging
import sys
import time
from datetime import datetime as dt
from logging.config import fileConfig
from pathlib import Path
from platform import system

# third party library
import click
from PyQt5 import QtWidgets

# local library
from my_widget import MyWidget, Style


class App:
    def __init__(self, logging_conf):
        fileConfig(logging_conf)
        self.logger = logging.getLogger(__name__)
        logging.Formatter.converter = time.gmtime

        self.logger.info("Determining Operating System.")
        my_system = system()
        if my_system == "Linux":
            self.my_system = "Linux"
        elif my_system == "Windows":
            self.my_system = "Windows"
        else:
            self.logger.error(
                f"This program only supports Linux and Windows, not '{my_system}'."
            )
            sys.exit()

    def get_info(self):
        if self.my_system == "Linux":
            # local library
            from linux import system_info
        else:
            # local library
            from windows import system_info

        network_info = system_info.get_network_info()
        disk_info = system_info.get_disk_info()
        now = dt.utcnow().strftime(Style.utc_datetime_fmt)
        system_info = {
            "os": self.my_system,
            "creation_time": now,
            "network": network_info,
            "boot_disk": disk_info,
        }
        return system_info

    def save_info(self, system_info, path):
        json_data = json.dumps(system_info)
        self.logger.info("Saving info to file.")
        with open(path, "wt", encoding="utf-8") as fout:
            fout.write(json_data)


def _create_output_dir():
    file = Path(__file__)
    project = file.parent
    output = project / "output"
    log = output / "log"
    logging_conf = project / "configuration.ini"
    data_file = output / "system-info.json"

    paths = {
        "logging_conf": logging_conf,
        "data_file": data_file,
    }

    # create output and log directory
    if not Path.exists(log):
        Path.mkdir(log, parents=True)

    return paths


def _prettify_message(system_info):
    os = system_info["os"]
    networks = system_info["network"]
    boot_disk = system_info["boot_disk"]
    message = ""

    message += "NETWORK\n\n"
    for network in networks:
        message += (
            f"Name: {network['name']}\n"
            f"IP: {network['ip']}\n"
            f"MAC: {network['mac']}\n\n"
        )
    message += "\nBOOT DISK\n\n"
    if os == "Linux":
        message += (
            f"Mount Point: {boot_disk['mount_point']}\n"
            f"Serial Number: {boot_disk['serial_number']}\n"
        )
    else:
        message += (
            f"Device ID: {boot_disk['device_id']}\n"
            f"Index: {boot_disk['index']}\n"
            f"Serial Number: {boot_disk['serial_number']}\n"
        )
    return message


@click.command()
@click.option("--gui", "/gui", is_flag=True, help="Use gui version.")
def main(gui):
    paths = _create_output_dir()
    my_app = App(paths["logging_conf"])
    system_info = my_app.get_info()

    if gui:
        gui_app = QtWidgets.QApplication([])
        widget = MyWidget(my_app, paths)
        gui_app.exec_()
    else:
        pretty_message = _prettify_message(system_info)
        print(pretty_message)

    my_app.save_info(system_info, paths["data_file"])


if __name__ == "__main__":
    main()
