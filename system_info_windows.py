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

"""windows, console"""

# standard library
import json
import logging
import re
import subprocess
import time
from datetime import datetime as dt
from logging.handlers import RotatingFileHandler
from pathlib import Path

# third party library
import wmi

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
    stdoutdata, stderrdata = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()
    out = stdoutdata.decode().replace("\r", "")
    pattern = re.compile(r"\\Device\\Harddisk(?P<harddisk>[\d])+\\Partition(?P<partition>[\d])+")
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


def save_info(system_info):
    logger.info("Saving info to file.")
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
        "disk": disk_info,
    }
    save_info(system_info)
    print(system_info)


if __name__ == "__main__":
    main()
