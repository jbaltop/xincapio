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

"""linux, console"""

# standard library
import fcntl
import json
import logging
import re
import shlex
import struct
import subprocess
import time
from datetime import datetime as dt
from logging.handlers import RotatingFileHandler
from pathlib import Path

# third party library
import netifaces as ni

UTC_DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

# file path
FILE = Path(__file__)
PROJECT = FILE.parent
OUTPUT = PROJECT / "output"
LOG = OUTPUT / "log"
LOG_FILE = LOG / f"{FILE.stem}.log"
DATA_FILE = OUTPUT / "system_info.json"

# create log directory
if not Path.exists(LOG):
    Path.mkdir(LOG, parents=True)

# create logger, set logging level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# set time zone to utc
logging.Formatter.converter = time.gmtime

# create file handler
fh = RotatingFileHandler(
    LOG_FILE, "at", encoding="utf-8", maxBytes=50 * 1024 * 1024, backupCount=5
)
fh.setLevel(logging.DEBUG)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
fh_formatter = logging.Formatter(
    "%(asctime)s UTC - %(name)s - %(levelname)s - %(message)s"
)
ch_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

# add formatter
fh.setFormatter(fh_formatter)
ch.setFormatter(ch_formatter)

# add the handler to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def get_network_info():
    logger.info("Getting network info.")
    interfaces = ni.interfaces()
    network_info = []
    for interface in interfaces:
        if_addresses = ni.ifaddresses(interface)
        mac = if_addresses[ni.AF_LINK][0]["addr"]
        ip = if_addresses[ni.AF_INET][0]["addr"]
        network_info.append({
            "name": interface,
            "ip": ip,
            "mac": mac,
        })
    return network_info


def get_disk_info():
    logger.info("Getting disk info.")
    out = subprocess.Popen(shlex.split("df /"), stdout=subprocess.PIPE).communicate()
    m = re.search(r'(/[^\s]+)\s', str(out))
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

    disk_info = {
        "mount_point": mount_point,
        "serial_number": serial_number,
    }
    return disk_info


def save_info(system_info):
    now = dt.utcnow().strftime(UTC_DATETIME_FMT)
    data = system_info.copy()
    data.update({"creation_time": now})
    json_data = json.dumps(data)
    with open(DATA_FILE, "wt", encoding="utf-8") as fout:
        fout.write(json_data)


def main():
    network_info = get_network_info()
    disk_info = get_disk_info()
    system_info = {
        "network": network_info,
        "boot_disk": disk_info,
    }
    save_info(system_info)
    print(system_info)


if __name__ == "__main__":
    main()
