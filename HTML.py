import requests
from bs4 import BeautifulSoup
import tkinter as tk
from dataclasses import dataclass

def get_value(string):
   return string['value']

def get_width(string):
   return int(string['width'].replace('%', '').replace(',', ''))

def get_height(string):
   return int(string['height'].replace('%', '').replace(',', ''))

def get_href(string):
   return string['href']

def get_src(string):
   if string['src'].startswith('//'):
       return string['src']
   else:
        return "http:" + string['src']

def get_type(string):
   return string['type']

def get_site(site, formated = 1):
   try:
       if site[0:8] == 'https://' and formated == 1:
           a = requests.get(site,verify=False, allow_redirects=True)
           s=BeautifulSoup(a.text, "lxml")
           return s
       elif site[0:8] == 'https://' and formated == 0:
           a = requests.get(site,verify=False, allow_redirects=True).content
           return a
       else:
           with open(site, "rb") as File:
               a = File.read()
               s=BeautifulSoup(a, "lxml")
               print(s)
               return s
   except requests.exceptions.ConnexionError():
      with open(site, "rb") as File:
         a = File.read()
         s=BeautifulSoup(a, "lxml")
         print(s)
         return s

def ok(site):
    if site[0:8] == 'https://':
        a = requests.get(site,verify=False, allow_redirects=True).ok
        return a
    else:
        return 1

@dataclass
class GraphicalObject:
    type: str = "Label"
    href: str = ""
    command: str = ""
    image: str = ""
    text: str = ""
    width: int = 0
    height: int = 0
    fg: str = "black"
    font_type: str = "Times New Roman"
    font_size: int = 16
    textvariable: tk.StringVar = None
    borderwidth: int = 2


class Ttk(tk.Tk):
   def __init__(self):
      self.exist = 1
      super().__init__()
      super().protocol("WM_DELETE_WINDOW", self.on_quit)

   def on_quit(self):
      self.exist = 0
      for widget in super().winfo_children():
        widget.destroy()
      super().destroy()
