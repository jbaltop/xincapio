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

# third party library
import wx
from wx.lib.scrolledpanel import ScrolledPanel


class Style:
    default_font = 10
    h1_font = 18

    default_border = 4
    h1_border = 100
    key_border = 30
    section_border = 25
    outer_border = 30


class ScrollPanel(ScrolledPanel):
    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent)

        self.SetupScrolling()


class MyFrame(wx.Frame):
    def __init__(self, parent, title, system_info):
        super(MyFrame, self).__init__(parent, title=title, size=(900, 600))

        self.system_info = system_info

        font = self.GetFont()
        font.SetPointSize(Style.default_font)
        self.SetFont(font)

        self.init_ui()
        self.Center()
        self.Show()

    def init_ui(self):
        panel = ScrollPanel(self)
        sizer = wx.GridBagSizer(0, 0)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        h1_font = wx.Font(Style.h1_font, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        key_font = wx.Font(Style.default_font, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        i = 0
        blank_space = wx.StaticLine(
            panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
        )
        sizer.Add(
            blank_space, pos=(i, 0), flag=wx.DOWN, border=Style.section_border
        )
        i += 1

        blank_space = wx.StaticLine(
            panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
        )
        sizer.Add(
            blank_space, pos=(i, 0), flag=wx.RIGHT, border=Style.section_border
        )

        line = wx.StaticText(panel, label="Network")
        line.SetFont(h1_font)
        sizer.Add(line, pos=(i, 1), span=(3, 1))

        blank_space = wx.StaticLine(
            panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
        )
        sizer.Add(
            blank_space, pos=(i, 2), flag=wx.RIGHT, border=Style.h1_border
        )

        for network in self.system_info["network"]:
            line = wx.StaticText(panel, label="Name")
            line.SetFont(key_font)
            sizer.Add(
                line,
                pos=(i, 3),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space, pos=(i, 4), flag=wx.RIGHT, border=Style.key_border
            )

            line = wx.StaticText(panel, label=network["name"])
            sizer.Add(
                line,
                pos=(i, 5),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space,
                pos=(i, 6),
                flag=wx.RIGHT,
                border=Style.section_border,
            )
            i += 1

            line = wx.StaticText(panel, label="IP")
            line.SetFont(key_font)
            sizer.Add(
                line,
                pos=(i, 3),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space, pos=(i, 4), flag=wx.RIGHT, border=Style.key_border
            )

            line = wx.StaticText(panel, label=network["ip"])
            sizer.Add(
                line,
                pos=(i, 5),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space,
                pos=(i, 6),
                flag=wx.RIGHT,
                border=Style.section_border,
            )
            i += 1

            line = wx.StaticText(panel, label="MAC")
            line.SetFont(key_font)
            sizer.Add(
                line,
                pos=(i, 3),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space, pos=(i, 4), flag=wx.RIGHT, border=Style.key_border
            )

            line = wx.StaticText(panel, label=network["mac"])
            sizer.Add(
                line,
                pos=(i, 5),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space,
                pos=(i, 6),
                flag=wx.RIGHT,
                border=Style.section_border,
            )
            i += 1

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space,
                pos=(i, 0),
                flag=wx.DOWN,
                border=Style.section_border,
            )
            i += 1

        hline = wx.StaticLine(panel, 0, size=(20, 1), style=wx.LI_HORIZONTAL)
        sizer.Add(
            hline, pos=(i, 0), span=(1, 7), flag=wx.ALIGN_CENTER | wx.EXPAND
        )
        i += 1

        blank_space = wx.StaticLine(
            panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
        )
        sizer.Add(
            blank_space, pos=(i, 0), flag=wx.DOWN, border=Style.section_border
        )
        i += 1

        blank_space = wx.StaticLine(
            panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
        )
        sizer.Add(
            blank_space, pos=(i, 0), flag=wx.RIGHT, border=Style.section_border
        )

        line = wx.StaticText(panel, label="Boot Disk")
        line.SetFont(h1_font)
        sizer.Add(line, pos=(i, 1), span=(3, 1))

        blank_space = wx.StaticLine(
            panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
        )
        sizer.Add(
            blank_space, pos=(i, 2), flag=wx.RIGHT, border=Style.h1_border
        )

        if self.system_info["os"] == "Linux":
            line = wx.StaticText(panel, label="Mount Point")
            line.SetFont(key_font)
            sizer.Add(
                line,
                pos=(i, 3),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space, pos=(i, 4), flag=wx.RIGHT, border=Style.key_border
            )

            line = wx.StaticText(
                panel, label=self.system_info["boot_disk"]["mount_point"]
            )
            sizer.Add(
                line,
                pos=(i, 5),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space,
                pos=(i, 6),
                flag=wx.RIGHT,
                border=Style.section_border,
            )
            i += 1

            line = wx.StaticText(panel, label="Serial Number")
            line.SetFont(key_font)
            sizer.Add(
                line,
                pos=(i, 3),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space, pos=(i, 4), flag=wx.RIGHT, border=Style.key_border
            )

            line = wx.StaticText(
                panel, label=str(self.system_info["boot_disk"]["serial_number"])
            )
            sizer.Add(
                line,
                pos=(i, 5),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

        else:
            line = wx.StaticText(panel, label="Device ID")
            line.SetFont(key_font)
            sizer.Add(
                line,
                pos=(i, 3),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space, pos=(i, 4), flag=wx.RIGHT, border=Style.key_border
            )

            line = wx.StaticText(
                panel, label=self.system_info["boot_disk"]["device_id"]
            )
            sizer.Add(
                line,
                pos=(i, 5),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space,
                pos=(i, 6),
                flag=wx.RIGHT,
                border=Style.section_border,
            )
            i += 1

            line = wx.StaticText(panel, label="Index")
            line.SetFont(key_font)
            sizer.Add(
                line,
                pos=(i, 3),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space, pos=(i, 4), flag=wx.RIGHT, border=Style.key_border
            )

            line = wx.StaticText(
                panel, label=str(self.system_info["boot_disk"]["index"])
            )
            sizer.Add(
                line,
                pos=(i, 5),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space,
                pos=(i, 6),
                flag=wx.RIGHT,
                border=Style.section_border,
            )
            i += 1

            line = wx.StaticText(panel, label="Serial Number")
            line.SetFont(key_font)
            sizer.Add(
                line,
                pos=(i, 3),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

            blank_space = wx.StaticLine(
                panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
            )
            sizer.Add(
                blank_space, pos=(i, 4), flag=wx.RIGHT, border=Style.key_border
            )

            line = wx.StaticText(
                panel, label=self.system_info["boot_disk"]["serial_number"]
            )
            sizer.Add(
                line,
                pos=(i, 5),
                flag=wx.UP | wx.DOWN,
                border=Style.default_border,
            )

        blank_space = wx.StaticLine(
            panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
        )
        sizer.Add(
            blank_space, pos=(i, 6), flag=wx.RIGHT, border=Style.section_border
        )
        i += 1

        blank_space = wx.StaticLine(
            panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
        )
        sizer.Add(
            blank_space, pos=(i, 0), flag=wx.DOWN, border=Style.section_border
        )
        i += 1

        # Add margin to left and right side
        blank_space = wx.StaticLine(
            panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
        )
        hbox.Add(blank_space, 0, flag=wx.RIGHT, border=Style.outer_border)

        hbox.Add(sizer)

        blank_space = wx.StaticLine(
            panel, 0, size=(0, 0), style=wx.LI_HORIZONTAL
        )
        hbox.Add(blank_space, 0, flag=wx.RIGHT, border=Style.outer_border)

        vbox.Add(hbox, 1, flag=wx.ALIGN_CENTER)

        panel.SetSizer(vbox)
