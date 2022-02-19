#! /usr/bin/python3

import os
import wx
import numpy as np
import math as ma
import scripts.cpp

class appframe(wx.Frame) : #inherent all properties from wx.Frame
    def __init__(self):
        super().__init__(parent=None, title='Air-CPP Generator')
        
        panel = wx.Panel(self) # this is one instance of panel within the frame
        sizer = wx.BoxSizer(wx.VERTICAL) # this is one instance of sizer to control the size of the widgets on the panel 
        
        self.text_crtl = wx.TextCtrl(parent=panel)
        sizer.Add(self.text_crtl, 0, wx.ALL | wx.EXPAND, 5)
        
        btn = wx.Button(panel, label='enter')
        sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
              
        panel.SetSizer(sizer)
        
        
        self.Show()


if __name__ == '__main__':
    app = wx.App()
    frame = appframe()    
    app.MainLoop() #the app start will call this member function
    
    
    
    
# app = wx.App()
# frame = wx.Frame(parent=None, title='Hello World')
# frame.Show()
# app.MainLoop()
