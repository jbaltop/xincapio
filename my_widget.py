# Copyright (C) 2019 Hajun Park
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# third party library
from PyQt5 import QtWidgets, QtGui


class Style:
    default_font = 10
    h1_font = 18

    default_border = 10
    h1_border = 100
    key_border = 30
    section_border = 25


class MyWidget(QtWidgets.QWidget):
    def __init__(self, my_app):
        super().__init__()
        self.my_app = my_app
        self.system_info = self.my_app.get_info()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll_widget_contents = QtWidgets.QWidget()
        self.grid = QtWidgets.QGridLayout(self.scroll_widget_contents)
        self.scroll.setWidget(self.scroll_widget_contents)
        self.layout.addWidget(self.scroll)
        self.grid.setSpacing(0)

        self.setWindowTitle("System Information")
        self.resize(900, 600)
        self.show_info()
        self.show()

        self.my_app.save_info(self.system_info)

    def show_info(self):
        default_font = QtGui.QFont()
        default_font.setPointSize(Style.default_font)

        h1_font = QtGui.QFont()
        h1_font.setPointSize(Style.h1_font)
        h1_font.setBold(True)

        key_font = QtGui.QFont()
        default_font.setPointSize(Style.default_font)
        key_font.setBold(True)

        i = 0
        blank_space = QtWidgets.QSpacerItem(
            0,
            Style.section_border,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        blank_space = QtWidgets.QSpacerItem(
            Style.section_border,
            0,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)

        label = QtWidgets.QLabel("Network")
        label.setFont(h1_font)
        self.grid.addWidget(label, i, 2, 3, 1)

        blank_space = QtWidgets.QSpacerItem(
            Style.h1_border,
            0,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 3)

        for network in self.system_info["network"]:
            label = QtWidgets.QLabel("Name")
            label.setFont(key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QtWidgets.QSpacerItem(
                Style.key_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QtWidgets.QLabel(network["name"])
            self.grid.addWidget(label, i, 6)

            blank_space = QtWidgets.QSpacerItem(
                Style.section_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QtWidgets.QSpacerItem(
                0,
                Style.default_border,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 4)
            i += 1

            label = QtWidgets.QLabel("IP")
            label.setFont(key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QtWidgets.QSpacerItem(
                Style.key_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QtWidgets.QLabel(network["ip"])
            self.grid.addWidget(label, i, 6)

            blank_space = QtWidgets.QSpacerItem(
                Style.default_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QtWidgets.QSpacerItem(
                0,
                Style.default_border,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 4)
            i += 1

            label = QtWidgets.QLabel("MAC")
            label.setFont(key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QtWidgets.QSpacerItem(
                Style.key_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QtWidgets.QLabel(network["mac"])
            self.grid.addWidget(label, i, 6)

            blank_space = QtWidgets.QSpacerItem(
                Style.section_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QtWidgets.QSpacerItem(
                0,
                Style.section_border,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 1)
            i += 1

        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.grid.addWidget(hline, i, 1, 1, 7)
        i += 1

        blank_space = QtWidgets.QSpacerItem(
            0,
            Style.section_border,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        blank_space = QtWidgets.QSpacerItem(
            Style.section_border,
            0,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)

        label = QtWidgets.QLabel("Boot Disk")
        label.setFont(h1_font)
        self.grid.addWidget(label, i, 2, 3, 1)

        blank_space = QtWidgets.QSpacerItem(
            Style.h1_border,
            0,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 3)

        if self.system_info["os"] == "Linux":
            label = QtWidgets.QLabel("Mount Point")
            label.setFont(key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QtWidgets.QSpacerItem(
                Style.key_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QtWidgets.QLabel(
                self.system_info["boot_disk"]["mount_point"]
            )
            self.grid.addWidget(label, i, 6)

            blank_space = QtWidgets.QSpacerItem(
                Style.section_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QtWidgets.QSpacerItem(
                0,
                Style.default_border,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 4)
            i += 1

            label = QtWidgets.QLabel("Serial Number")
            label.setFont(key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QtWidgets.QSpacerItem(
                Style.key_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QtWidgets.QLabel(
                self.system_info["boot_disk"]["serial_number"]
            )
            self.grid.addWidget(label, i, 6)

        else:
            label = QtWidgets.QLabel("Device ID")
            label.setFont(key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QtWidgets.QSpacerItem(
                Style.key_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QtWidgets.QLabel(self.system_info["boot_disk"]["device_id"])
            self.grid.addWidget(label, i, 6)

            blank_space = QtWidgets.QSpacerItem(
                Style.section_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QtWidgets.QSpacerItem(
                0,
                Style.default_border,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 4)
            i += 1

            label = QtWidgets.QLabel("Index")
            label.setFont(key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QtWidgets.QSpacerItem(
                Style.key_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QtWidgets.QLabel(
                str(self.system_info["boot_disk"]["index"])
            )
            self.grid.addWidget(label, i, 6)

            blank_space = QtWidgets.QSpacerItem(
                Style.section_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QtWidgets.QSpacerItem(
                0,
                Style.default_border,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 4)
            i += 1

            label = QtWidgets.QLabel("Serial Number")
            label.setFont(key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QtWidgets.QSpacerItem(
                Style.key_border,
                0,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QtWidgets.QLabel(
                self.system_info["boot_disk"]["serial_number"]
            )
            self.grid.addWidget(label, i, 6)

        blank_space = QtWidgets.QSpacerItem(
            Style.section_border,
            0,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 7)

        blank_space = QtWidgets.QSpacerItem(
            0,
            Style.section_border,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)

        i += 1
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(8, 1)
        self.grid.setRowStretch(i, 1)
