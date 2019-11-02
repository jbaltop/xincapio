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
import logging
import re
import subprocess

# third party library
import wmi

logger = logging.getLogger(__name__)


def get_network_info():
    logger.info("Getting network info.")
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


def get_disk_info():
    logger.info("Getting boot disk caption.")
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

    logger.info("Getting boot disk serial number.")
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
