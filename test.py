#! /usr/bin/python3

import os
from turtle import title
import wx
import scripts.cpp as cpp


class test:
    
    def __init__(self):
        self.a = 2
        self.b = 4
        

class what(test): 
    # class a(class b) (class a will then inherent all the variables and function from class b)
    
    def __init__(self):
        super().__init__()
        self.z = 0
        





class Person:
    
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname
        l = cpp.tool.datatype ()
        

    def printname(self):
        print(self.firstname, self.lastname)
        
class Student(Person):
    
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)
        self.graduationyear = year

    def welcome(self):
        print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)






class mainframe(wx.Frame): 
    #inherent all the wx.frame into this mainframe class
    
    def __init__(self):
        super().__init__(parent=None, title='Air Mission Planner')
        self.Show()

     
if __name__ == '__main__':
    app = wx.App()
    frame = mainframe()
    app.MainLoop()
        