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
import fcntl
import logging
import re
import shlex
import struct
import subprocess

# third party library
import netifaces as ni


class SystemInfo:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_network_info(self):
        self.logger.info("Getting network info.")
        interfaces = ni.interfaces()
        network_info = []
        for interface in interfaces:
            if_addresses = ni.ifaddresses(interface)
            mac = if_addresses[ni.AF_LINK][0]["addr"]
            ip = if_addresses[ni.AF_INET][0]["addr"]
            network_info.append({"name": interface, "ip": ip, "mac": mac})
        return network_info

    def get_disk_info(self):
        self.logger.info("Getting boot disk mount point.")
        out = subprocess.Popen(
            shlex.split("df /"), stdout=subprocess.PIPE
        ).communicate()
        m = re.search(r"(/[^\s]+)\s", str(out))
        mount_point = m.group(1)

        self.logger.info("Getting boot disk serial number.")
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
