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
from datetime import datetime as dt

# third party library
from dateutil import tz
from PyQt5.QtCore import (
    QUrl,
)
from PyQt5.QtGui import (
    QDesktopServices,
    QFont,
    QIcon,
)
from PyQt5.QtWidgets import (
    QAction,
    qApp,
    QDialog,
    QFileDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QHBoxLayout,
    QMainWindow,
    QSizePolicy,
    QScrollArea,
    QSpacerItem,
    QWidget,
)


class Style:
    utc_datetime_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    local_datetime_fmt = "%Y-%m-%d %H:%M:%S.%f"

    default_typeface_win = "Segoe UI"
    mono_typeface_win = "Consolas"
    mono_typeface_linux = "DejaVu Sans Mono"

    default_font = 10
    h1_font = 18

    default_border = 10
    h1_border = 100
    key_border = 30
    section_border = 25


class MyWidget(QMainWindow):
    def __init__(self, my_app):
        super().__init__()
        self.my_app = my_app
        self.paths = self.my_app.paths

        self.setWindowTitle("Xincapio")
        self.resize(900, 600)
        self.show()

        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        save_button = QAction(QIcon(), "&Save", self)
        save_button.setShortcut("Ctrl+S")
        save_button.triggered.connect(self.on_save)
        file_menu.addAction(save_button)

        refresh_button = QAction(QIcon(), "&Refresh", self)
        refresh_button.setShortcut("Ctrl+R")
        refresh_button.triggered.connect(self.init_ui)
        file_menu.addAction(refresh_button)

        exit_button = QAction(QIcon(), "&Exit", self)
        exit_button.setShortcut("Ctrl+Q")
        exit_button.triggered.connect(qApp.quit)
        file_menu.addAction(exit_button)

        help_menu = menubar.addMenu("&Help")

        about_button = QAction(QIcon(), "&About", self)
        about_button.triggered.connect(self.on_about)
        help_menu.addAction(about_button)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self)
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll_widget_contents = QWidget()
        self.grid = QGridLayout(self.scroll_widget_contents)
        self.scroll.setWidget(self.scroll_widget_contents)
        self.layout.addWidget(self.scroll)
        self.grid.setSpacing(0)

        self.default_font = QFont()
        self.default_font.setPointSize(Style.default_font)

        self.h1_font = QFont()
        self.h1_font.setPointSize(Style.h1_font)
        self.h1_font.setBold(True)

        self.key_font = QFont()
        self.key_font.setPointSize(Style.default_font)
        self.key_font.setBold(True)

        if self.my_app.my_system == "Windows":
            self.default_font.setFamily(Style.default_typeface_win)
            self.h1_font.setFamily(Style.default_typeface_win)
            self.key_font.setFamily(Style.default_typeface_win)

        self.centralWidget().setLayout(self.layout)

        self.init_ui()

    def init_ui(self):
        self.system_info = self.my_app.get_info()
        self.show_info()

    def show_info(self):
        if self.grid.count():
            for index in reversed(range(self.grid.count())):
                widget_to_remove = self.grid.itemAt(index).widget()
                if widget_to_remove:
                    self.grid.removeWidget(widget_to_remove)
                    widget_to_remove.setParent(None)
                else:
                    self.grid.removeItem(self.grid.itemAt(index))

        i = 0
        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        blank_space = QSpacerItem(
            Style.section_border,
            0,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)

        label = QLabel("Network")
        label.setFont(self.h1_font)
        self.grid.addWidget(label, i, 2, 3, 1)

        blank_space = QSpacerItem(
            Style.h1_border,
            0,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 3)

        for network in self.system_info["network"]:
            label = QLabel("Name")
            label.setFont(self.key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QSpacerItem(
                Style.key_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QLabel(network["name"])
            label.setFont(self.default_font)
            self.grid.addWidget(label, i, 6)

            blank_space = QSpacerItem(
                Style.section_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QSpacerItem(
                0,
                Style.default_border,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 4)
            i += 1

            label = QLabel("IP")
            label.setFont(self.key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QSpacerItem(
                Style.key_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QLabel(network["ip"])
            label.setFont(self.default_font)
            self.grid.addWidget(label, i, 6)

            blank_space = QSpacerItem(
                Style.default_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QSpacerItem(
                0,
                Style.default_border,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 4)
            i += 1

            label = QLabel("MAC")
            label.setFont(self.default_font)
            label.setFont(self.key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QSpacerItem(
                Style.key_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QLabel(network["mac"])
            label.setFont(self.default_font)
            self.grid.addWidget(label, i, 6)

            blank_space = QSpacerItem(
                Style.section_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QSpacerItem(
                0,
                Style.section_border,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 1)
            i += 1

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        self.grid.addWidget(hline, i, 1, 1, 7)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        blank_space = QSpacerItem(
            Style.section_border,
            0,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)

        label = QLabel("Boot Disk")
        label.setFont(self.h1_font)
        self.grid.addWidget(label, i, 2, 3, 1)

        blank_space = QSpacerItem(
            Style.h1_border,
            0,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 3)

        if self.system_info["os"] == "Linux":
            label = QLabel("Mount Point")
            label.setFont(self.key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QSpacerItem(
                Style.key_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QLabel(
                self.system_info["boot_disk"]["mount_point"]
            )
            label.setFont(self.default_font)
            self.grid.addWidget(label, i, 6)

            blank_space = QSpacerItem(
                Style.section_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QSpacerItem(
                0,
                Style.default_border,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 4)
            i += 1

            label = QLabel("Serial Number")
            label.setFont(self.key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QSpacerItem(
                Style.key_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QLabel(
                self.system_info["boot_disk"]["serial_number"]
            )
            label.setFont(self.default_font)
            self.grid.addWidget(label, i, 6)

        else:
            label = QLabel("Device ID")
            label.setFont(self.key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QSpacerItem(
                Style.key_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QLabel(self.system_info["boot_disk"]["device_id"])
            label.setFont(self.default_font)
            self.grid.addWidget(label, i, 6)

            blank_space = QSpacerItem(
                Style.section_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QSpacerItem(
                0,
                Style.default_border,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 4)
            i += 1

            label = QLabel("Index")
            label.setFont(self.key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QSpacerItem(
                Style.key_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QLabel(
                str(self.system_info["boot_disk"]["index"])
            )
            label.setFont(self.default_font)
            self.grid.addWidget(label, i, 6)

            blank_space = QSpacerItem(
                Style.section_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 7)
            i += 1

            blank_space = QSpacerItem(
                0,
                Style.default_border,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 4)
            i += 1

            label = QLabel("Serial Number")
            label.setFont(self.key_font)
            self.grid.addWidget(label, i, 4)

            blank_space = QSpacerItem(
                Style.key_border,
                0,
                QSizePolicy.Minimum,
                QSizePolicy.Minimum,
            )
            self.grid.addItem(blank_space, i, 5)

            label = QLabel(
                self.system_info["boot_disk"]["serial_number"]
            )
            label.setFont(self.default_font)
            self.grid.addWidget(label, i, 6)

        blank_space = QSpacerItem(
            Style.section_border,
            0,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 7)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        local_time = _convert_timezone(self.system_info["creation_time"])
        message = "Updated at " + str(local_time)
        self.statusBar().showMessage(message)

        i += 1
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(8, 1)
        self.grid.setRowStretch(i, 1)

    def on_save(self):
        output_file = QFileDialog.getSaveFileName(
            self,
            filter="All Files (*);;JSON (*.json)",
            initialFilter="JSON (*.json)",
            directory="/",
        )
        output_path, file_type = output_file
        if output_path != "":
            self.my_app.save_info(self.system_info, output_path)

    def on_about(self):
        dialog = AboutDialog(self.paths, self.system_info["os"], self)
        dialog.exec_()


class AboutDialog(QDialog):
    def __init__(self, paths, os, parent=None):
        super().__init__(parent)

        self.paths = paths
        self.os = os

        self.setWindowTitle("About")
        self.resize(750, 500)
        self.show()

        self.layout = QHBoxLayout(self)
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll_widget_contents = QWidget()
        self.grid = QGridLayout(self.scroll_widget_contents)
        self.scroll.setWidget(self.scroll_widget_contents)
        self.layout.addWidget(self.scroll)

        self.default_font = QFont()
        self.default_font.setPointSize(Style.default_font)

        self.h1_font = QFont()
        self.h1_font.setPointSize(Style.h1_font)
        self.h1_font.setBold(True)

        if self.os == "Linux":
            self.default_font.setFamily(Style.mono_typeface_linux)
        else:
            self.default_font.setFamily(Style.mono_typeface_win)
            self.h1_font.setFamily(Style.default_typeface_win)

        self.init_ui()

    def init_ui(self):
        i = 0
        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        label = QLabel("Xincapio")
        label.setFont(self.h1_font)
        self.grid.addWidget(label, i, 1)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        label = QLabel("Get IP address, MAC address and Disk Serial Number")
        label.setFont(self.default_font)
        self.grid.addWidget(label, i, 1)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        self.grid.addWidget(hline, i, 1)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        label = QLabel("Developer")
        label.setFont(self.h1_font)
        self.grid.addWidget(label, i, 1)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        label = QLabel("Hajun Park")
        label.setFont(self.default_font)
        self.grid.addWidget(label, i, 1)
        i += 1

        label = QLabel('<a href="mailto:jbaltop@gmail.com">jbaltop@gmail.com</a>')
        label.setFont(self.default_font)
        label.linkActivated.connect(self.open_link)
        self.grid.addWidget(label, i, 1)
        i += 1

        label = QLabel('<a href="https://github.com/jbaltop">https://github.com/jbaltop</a>')
        label.setFont(self.default_font)
        label.linkActivated.connect(self.open_link)
        self.grid.addWidget(label, i, 1)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        self.grid.addWidget(hline, i, 1)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        label = QLabel("Version")
        label.setFont(self.h1_font)
        self.grid.addWidget(label, i, 1)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        with open(self.paths["version"], encoding="utf-8") as fin:
            version = fin.read()[:-1]
        label = QLabel(version)
        label.setFont(self.default_font)
        self.grid.addWidget(label, i, 1)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        self.grid.addWidget(hline, i, 1)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        label = QLabel("License")
        label.setFont(self.h1_font)
        self.grid.addWidget(label, i, 1)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)
        i += 1

        with open(self.paths["license"], encoding="utf-8") as fin:
            license = fin.read()
        label = QLabel(license)
        label.setFont(self.default_font)
        self.grid.addWidget(label, i, 1)
        i += 1

        blank_space = QSpacerItem(
            0,
            Style.section_border,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum,
        )
        self.grid.addItem(blank_space, i, 1)

        i += 1
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(2, 1)
        self.grid.setRowStretch(i, 1)

    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))


def _convert_timezone(from_time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    from_time = dt.strptime(from_time, Style.utc_datetime_fmt)
    from_time = from_time.replace(tzinfo=from_zone)
    to_time = from_time.astimezone(to_zone)
    to_time = to_time.strftime(Style.local_datetime_fmt)
    return to_time
