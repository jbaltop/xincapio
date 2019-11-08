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
import fcntl
import re
import shlex
import struct
import subprocess

# third party library
import netifaces as ni


def get_network_info():
    interfaces = ni.interfaces()
    network_info = []
    for interface in interfaces:
        if_addresses = ni.ifaddresses(interface)
        mac = if_addresses[ni.AF_LINK][0]["addr"]
        ip = if_addresses[ni.AF_INET][0]["addr"]
        network_info.append({"name": interface, "ip": ip, "mac": mac})
    return network_info


def get_disk_info():
    out = subprocess.Popen(
        shlex.split("df /"), stdout=subprocess.PIPE
    ).communicate()
    m = re.search(r"(/[^\s]+)\s", str(out))
    mount_point = m.group(1)

    with open(mount_point, "rb") as fd:
        # tediously derived from the monster struct defined in <hdreg.h>
        # see comment at end of file to verify
        hd_driveid_format_str = (
            "@ 10H 20s 3H 8s 40s 2B H 2B H 4B 6H 2B I 36H I Q 152H"
        )
        # Also from <hdreg.h>
        HDIO_GET_IDENTITY = 0x030D
        # How big a buffer do we need?
        sizeof_hd_driveid = struct.calcsize(hd_driveid_format_str)

        # ensure our format string is the correct size
        # 512 is extracted using sizeof(struct hd_id) in the c code
        assert sizeof_hd_driveid == 512

        # Call native function
        buf = fcntl.ioctl(fd, HDIO_GET_IDENTITY, " " * sizeof_hd_driveid)
        fields = struct.unpack(hd_driveid_format_str, buf)
        serial_number = fields[10].strip().decode()

    disk_info = {"mount_point": mount_point, "serial_number": serial_number}
    return disk_info
