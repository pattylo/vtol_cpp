#! /usr/bin/python3
import wx

class LeftPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        label = "Buttons"
        lbl = wx.StaticText(self, label=label)

        self.attach_btn = wx.Button(self, -1, "Select",size = (150,25))
        self.Bind(wx.EVT_BUTTON, self.OnOpen, self.attach_btn)

        self.remove_btn = wx.Button(self, -1, "Remove")
        self.Bind(wx.EVT_BUTTON, self.OnRemove, self.remove_btn)

        v_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(v_sizer, 0, wx.ALL, 5)
        sizer.Add(lbl, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.attach_btn,0, wx.ALL |wx.EXPAND , 3)
        sizer.Add(self.remove_btn,0, wx.ALL |wx.EXPAND, 3)

        self.SetSizer(sizer)

    def OnOpen(self, event):
        print('do something')


    def OnRemove(self,event):
        print('do something else')

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        v_sizer = wx.BoxSizer(wx.VERTICAL)

        left_panel = LeftPanel(self)
        hsizer.Add(left_panel,1,wx.EXPAND)

        self.done_btn = wx.Button(self, -1, "DONE")
        self.Bind(wx.EVT_BUTTON, self.OnDone, self.done_btn)

        v_sizer.Add(hsizer, 1, wx.EXPAND)
        v_sizer.Add(self.done_btn,0, wx.ALL |wx.CENTER, 3)

        self.SetSizer(v_sizer)

    def OnDone(self,event):
        self.Close()
        self.Parent.Destroy()

class NewFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="New mission")
        panel = MainPanel(self)
        self.SetWindowStyle(wx.STAY_ON_TOP)
        self.Show()
