#!/usr/bin/env python3

import wx
from test import NewFrame

class TopFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Test")
        
        self.panel = wx.Panel(self)
        self.call_button = wx.Button(self.panel, label="Call Popup")
        self.call_button.Bind(wx.EVT_BUTTON, self.popup)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel)
        self.SetSizer(sizer)
        self.Show()

    def popup(self, event):
        pop = NewFrame()

if __name__ == "__main__":
    app = wx.App()
    frame2 = TopFrame()
    app.MainLoop()
