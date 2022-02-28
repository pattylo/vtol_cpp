#!/usr/bin/env python3

import wx
class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Dialog Test",size=(500,400))
        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.log = wx.TextCtrl(self.panel, wx.ID_ANY, size=(400,300),style = wx.TE_MULTILINE|wx.TE_READONLY|wx.VSCROLL)
        self.button = wx.Button(self.panel, label="Click me")
        sizer.Add(self.log, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.button, 0, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self,event):
        dlg = GetData(parent = self.panel) 
        dlg.ShowModal()
        if dlg.result_name:
            self.log.AppendText("Name: "+dlg.result_name+"\n")
            self.log.AppendText("Surname: "+dlg.result_surname+"\n")
            self.log.AppendText("Nickname: "+dlg.result_nickname+"\n")
        else:
            self.log.AppendText("No Input found\n")
        dlg.Destroy()

class GetData(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Parameters Input", size= (560,800))
        self.panel = wx.Panel(self,wx.ID_ANY)



        self.one = wx.StaticText(self.panel, label="1st point", pos=(120,20))
        self.onee = wx.TextCtrl(self.panel, value="", pos=(260,20), size=(140,-1))
        self.two = wx.StaticText(self.panel, label="2nd point", pos=(120,60))
        self.twoo = wx.TextCtrl(self.panel, value="", pos=(260,60), size=(140,-1))
        self.three = wx.StaticText(self.panel, label="3rd point", pos=(120,100))
        self.threee = wx.TextCtrl(self.panel, value="", pos=(260,100), size=(140,-1))
        self.four = wx.StaticText(self.panel, label="4th point", pos=(120,140))
        self.fourr = wx.TextCtrl(self.panel, value="", pos=(260,140), size=(140,-1))
        self.five = wx.StaticText(self.panel, label="min altitude", pos=(120,180))
        self.fivee = wx.TextCtrl(self.panel, value="", pos=(260,180), size=(140,-1))
        self.six = wx.StaticText(self.panel, label="max altitude", pos=(120,220))
        self.sixx = wx.TextCtrl(self.panel, value="", pos=(260,220), size=(140,-1))
        self.seven = wx.StaticText(self.panel, label="sampling density", pos=(120,260))
        self.sevenn = wx.TextCtrl(self.panel, value="", pos=(260,260), size=(140,-1))
        
        # bmp = wx.Bitmap('qgc.png') 
        self.saveButton =wx.Button(self.panel, label="cycle-Boustrophedon", pos=(110,320))
        # self.saveButton.SetBitmap(bmp)
        self.closeButton =wx.Button(self.panel, label="cycling-foward", pos=(310,320))
        # self.lalaButton =wx.Button(self.panel, label="Cancel", pos=(310,320))       
        
        
        self.saveButton =wx.Button(self.panel, label="QGC", pos=(110,360))
        # self.saveButton.SetBitmap(bmp)
        self.closeButton =wx.Button(self.panel, label="MP", pos=(210,360))
        self.lalaButton =wx.Button(self.panel, label="Cancel", pos=(310,360))

        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        
        imageFile = 'vtol.png'
        png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # self.bump = wx.StaticBitmap(self, -1, png, pos=(310,400))
        
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.Show()
        
    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()
 
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap('vtol.png')
        dc.DrawBitmap(bmp, 0, 0)

    def OnQuit(self, event):
        self.result_name = None
        self.Destroy()

    def SaveConnString(self, event):
        self.result_name = self.name.GetValue()
        self.result_surname = self.surname.GetValue()
        self.result_nickname = self.nickname.GetValue()
        self.Destroy()

app = wx.App()
frame = MyFrame(None)
frame.Show()
app.MainLoop()