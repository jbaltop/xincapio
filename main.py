# Copyright (C) 2019 Hajun Park
#
# This file is part of Xincapio
#
# Xincapio is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Xincapio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# standard library
import json
import sys
from datetime import datetime as dt
from pathlib import Path
from platform import system

# third party library
import click
from PyQt5 import QtWidgets

# local library
from console_app import ConsoleApp
from my_widget import MyWidget, Style


class App:
    def __init__(self, paths):
        self.paths = paths

        my_system = system()
        if my_system == "Linux":
            self.my_system = "Linux"
        elif my_system == "Windows":
            self.my_system = "Windows"
        else:
            print(
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
        with open(path, "wt", encoding="utf-8") as fout:
            fout.write(json_data)


def get_path():
    # project
    file = Path(__file__)
    project = file.parent

    # existing file
    version = project / "version.txt"
    license = project / "LICENSE"

    paths = {
        "license": license,
        "version": version,
    }

    return paths


@click.command()
@click.option("--gui", "/gui", is_flag=True, help="Use gui version.")
@click.option("--output", "/output", help="Specify path to output file.")
@click.option("--version", "/version", is_flag=True, help="Show version.")
def main(gui, output, version):
    paths = get_path()

    if version:
        with open(paths["version"], encoding="utf-8") as fin:
            print(fin.read()[:-1])
        return

    my_app = App(paths)

    if gui:
        gui_app = QtWidgets.QApplication([])
        widget = MyWidget(my_app)
        gui_app.exec_()
    else:
        console_app = ConsoleApp(my_app, output)
        console_app.run()


if __name__ == "__main__":
    main()
