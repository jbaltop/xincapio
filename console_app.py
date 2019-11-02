# Copyright (C) 2019 Hajun Park
#
# This file is part of System Information
#
# System Information is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# System Information is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# standard library
from pathlib import Path


class ConsoleApp:
    def __init__(self, my_app, output):
        self.my_app = my_app
        self.output = output
        self.paths = self.my_app.paths
        self.system_info = self.my_app.get_info()

    def prettify_message(self):
        os = self.system_info["os"]
        networks = self.system_info["network"]
        boot_disk = self.system_info["boot_disk"]
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

    def run(self):
        message = self.prettify_message()
        print(message)

        if self.output:
            output_path = Path(self.output)
            if output_path.exists():
                self.path_exists(output_path)
            else:
                self.path_not_exists(output_path)
        else:
            self.my_app.save_info(self.system_info, self.paths["data_file"])

    def path_exists(self, output_path):
        overwrite = input(
            f"'{output_path}' already exsists. Do you want to overwrite [y/N]? "
        )
        if overwrite == "y":
            self.my_app.save_info(self.system_info, output_path)
        else:
            return

    def path_not_exists(self, output_path):
        if not output_path.parent.exists():
            Path.mkdir(output_path.parent, parents=True)
        self.my_app.save_info(self.system_info, output_path)
