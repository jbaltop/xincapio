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
import os.path
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import time
import winreg as wr

# related third party imports
import netifaces
import wmi

# registry path for network interface names
REG_KEY = wr.HKEY_LOCAL_MACHINE
REG_NETWORK = "SYSTEM\\CurrentControlSet\\Control\\Network\\{4d36e972-e325-11ce-bfc1-08002be10318}"

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

CHUNK = 4096


def main():
    logger.info("Start system_info")
    network_info = get_network_info()
    for i in network_info:
        num = netifaces.AF_LINK
        if num in i["if_addresses"]:
            print(i["if_addresses"][num])
    hdd_info = get_hdd_info()
    print(f"hdd info: {hdd_info['tag']}, {hdd_info['serial_number']}")
    logger.info("End system_info")


def get_network_info():
    interfaces = netifaces.interfaces()
    info = []
    for interface in interfaces:
        logger.debug(f"interface: {interface}")
        if_addresses = netifaces.ifaddresses(interface)
        logger.debug(f"if_addresses: {if_addresses}")
        if_name = _get_interface_name(interface)
        info.append({
            "interface": interface,
            "if_name": if_name,
            "if_addresses": if_addresses,
        })
        # if netifaces.AF_INET in ifaddresses:
        #     ifaddress = ifaddresses[netifaces.AF_INET]
        #     return(f"interface: {interface}, ifaddress: {ifaddress}")

        # MAC: info["if_addresses"][-1000][0]["addr"]
        # -1000 = netifaces.AF_LINK
        # IP: info["if_addresses"][2][0]["addr"]
        # 2 = netifaces.AF_INET
    return info


def _get_interface_name(interface_id):
    subkey = os.path.join(REG_NETWORK, interface_id, "Connection")
    value_name = "Name"
    try:
        with wr.OpenKey(REG_KEY, subkey) as key:
            interface_name = wr.QueryValueEx(key, value_name)[0]
            logger.debug(f"interface_name: {interface_name}")
    except FileNotFoundError:
        return None
    return interface_name


def get_hdd_info():
    conn = wmi.WMI()
    for item in conn.Win32_PhysicalMedia():
        if item.Tag == "\\\\.\\PHYSICALDRIVE0":
            hdd_info = {
                "tag": item.Tag,
                "serial_number": item.SerialNumber,
            }
            return hdd_info


if __name__ == "__main__":
    main()
