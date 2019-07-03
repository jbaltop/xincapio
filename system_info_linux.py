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
import logging
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

# third party
import netifaces as ni
from blkinfo import BlkDiskInfo

DISK_NAME = "sda"

FILE = Path(__file__)
PROJECT = FILE.parent
OUTPUT = PROJECT / "output"
LOG = OUTPUT / "log"
LOG_FILE = LOG / f"{FILE.stem}.log"

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
    myblkd = BlkDiskInfo()
    disks = myblkd.get_disks()
    for disk in disks:
        if disk["type"] == "disk":
            if disk["name"] == DISK_NAME:
                disk_info = {
                    "name": DISK_NAME,
                    "serial_number": disk["serial"],
                }
                return disk_info


def main():
    network_info = get_network_info()
    disk_info = get_disk_info()
    print(network_info)
    print(disk_info)


if __name__== "__main__":
    main()
