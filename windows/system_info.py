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
import re
import subprocess

# third party library
import wmi


class SystemInfo:
    @staticmethod
    def get_network_info():
        conn = wmi.WMI()
        interfaces = conn.Win32_NetworkAdapterConfiguration()
        network_info = []
        for interface in interfaces:
            if interface.IPEnabled:
                network_info.append(
                    {
                        "name": interface.Description,
                        "ip": interface.IPAddress[0],
                        "mac": interface.MACAddress,
                    }
                )
        return network_info

    @staticmethod
    def get_disk_info():
        command = "wmic bootconfig get caption"
        stdoutdata, stderrdata = subprocess.Popen(
            command, stdout=subprocess.PIPE
        ).communicate()
        out = stdoutdata.decode().replace("\r", "")
        pattern = re.compile(
            r"\\Device\\Harddisk(?P<harddisk>[\d])+\\Partition(?P<partition>[\d])+"
        )
        result = pattern.search(out)
        disk_index = int(result.group("harddisk"))

        conn = wmi.WMI()
        for disk in conn.Win32_DiskDrive(["DeviceID", "Index", "SerialNumber"]):
            if disk.Index == disk_index:
                disk_info = {
                    "device_id": disk.DeviceID,
                    "index": disk.Index,
                    "serial_number": disk.SerialNumber,
                }
                return disk_info
        return None
