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

# windows, console

import netifaces
import winreg as wr
import os
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import time

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

# create logger
logger = logging.getLogger('system_info')
logger.setLevel(logging.INFO)

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
fh.setLevel(logging.INFO)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

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
    network_info = NetworkInfo()
    info = network_info.get_info()
    for i in info:
        print(i)


class NetworkInfo:
    def get_info(self):
        interfaces = netifaces.interfaces()
        info = []
        for interface in interfaces:
            if_address = netifaces.ifaddresses(interface)
            if_name = self.get_interface_name(interface)
            info.append({
                "interface": interface,
                "if_name": if_name,
                "if_addresses": if_address,
            })
            # if netifaces.AF_INET in ifaddresses:
            #     ifaddress = ifaddresses[netifaces.AF_INET]
            #     return(f"interface: {interface}, ifaddress: {ifaddress}")
        return info

    def get_interface_name(self, interface_id):
        subkey = os.path.join(REG_NETWORK, interface_id, "Connection")
        value_name = "Name"
        with wr.OpenKey(REG_KEY, subkey) as key:
            interface_name = wr.QueryValueEx(key, value_name)[0]
        return interface_name


if __name__ == "__main__":
    main()
