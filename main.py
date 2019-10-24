# Copyright 2019 Hajun Park
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
import wx

# local library
from my_frame import MyFrame


class App:
    def __init__(self):
        self.utc_datetime_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"

        file = Path(__file__)
        project = file.parent
        output = project / "output"
        log = output / "log"
        logging_conf = project / "configuration.ini"
        self.data_file = output / "system-info.json"

        # create output and log directory
        if not Path.exists(log):
            Path.mkdir(log, parents=True)

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
        now = dt.utcnow().strftime(self.utc_datetime_fmt)
        system_info = {
            "os": self.my_system,
            "creation_time": now,
            "network": network_info,
            "boot_disk": disk_info,
        }
        return system_info

    def save_info(self, system_info):
        json_data = json.dumps(system_info)
        self.logger.info("Saving info to file.")
        with open(self.data_file, "wt", encoding="utf-8") as fout:
            fout.write(json_data)


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
    my_app = App()
    system_info = my_app.get_info()

    if gui:
        gui_app = wx.App()
        MyFrame(None, "System Information", system_info)
        gui_app.MainLoop()
    else:
        pretty_message = _prettify_message(system_info)
        print(pretty_message)

    my_app.save_info(system_info)


if __name__ == "__main__":
    main()
