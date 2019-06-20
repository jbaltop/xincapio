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

# standard library imports
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import time

# related third party imports
import wmi

PHYSICAL_DISK_TAG = "\\\\.\\PHYSICALDRIVE0"

# create log directory
file = Path(__file__)
output_path = file.parent / "output"
log_path = output_path / "log"

if not output_path.exists():
    Path.mkdir(output_path)

if not log_path.exists():
    Path.mkdir(log_path)

# create logger, set logging level
logger = logging.getLogger('system_info')
logger.setLevel(logging.DEBUG)

# set time zone to utc
logging.Formatter.converter = time.gmtime

# create file handler
fh = RotatingFileHandler(
    'output/log/system_info.log',
    'at',
    encoding='utf-8',
    maxBytes=50*1024*1024,
    backupCount=5
)
fh.setLevel(logging.DEBUG)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s UTC - %(name)s - %(levelname)s - %(message)s'
)

# add formatter
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def main():
    network_info = get_network_info()
    physical_disk_info = get_physical_disk_info()
    print(network_info)
    print(physical_disk_info)


def get_network_info():
    conn = wmi.WMI()
    interfaces = conn.Win32_NetworkAdapterConfiguration()
    network_info = []
    for interface in interfaces:
        if interface.IPEnabled:
            network_info.append({
                "name": interface.Description,
                "ip": interface.IPAddress[0],
                "mac": interface.MACAddress,
            })
    return network_info


def get_physical_disk_info():
    conn = wmi.WMI()
    for item in conn.Win32_PhysicalMedia():
        if item.Tag == PHYSICAL_DISK_TAG:
            physical_disk_info = {
                "tag": PHYSICAL_DISK_TAG,
                "serial_number": item.SerialNumber,
            }
            return physical_disk_info


if __name__ == "__main__":
    main()
