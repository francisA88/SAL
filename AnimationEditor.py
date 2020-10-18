from kivy.uix.slider import Slider
from kivy.core.window import Window as win
#print(dir(win))
from kivymd.app import MDApp as App
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import ObjectProperty

from kivy.graphics import *

from stickman import StickMan
from parser.animationloader import Animloader as Al
from parser import animToXML
import os

from kivy.lang import Builder

win.softinput_mode = "below_target"
WHITE = (1,)*4
#win.clearcolor = WHITE
class SidePanel(Widget): pass
class BottomPanel(Widget): pass
class MainWindow(FloatLayout):
	cache_panel= ObjectProperty(None)
	app = ObjectProperty(None)
	def __init__(self, **kws):
		super().__init__(**kws)
		Clock.schedule_interval(lambda *args: setattr(self.cache_panel, "text", self.app.anim_string), .05)
		
class MyTextInput(TextInput):
	def do_backspace(self):
		super().do_backspace()
		l = self.cursor[0]
		t = self.text
		self.text = ""
		self.insert_text(t)
		self.cursor = l, 0

def isnumber(arg1,string):
	try:
		float(string)
	except ValueError:
		return False
	return True
	
class Editor(App):
	temp_anim_string = ""
	anim_string = ""
	position = win.center[0]-20, 2.3*win.height/3
	sm = StickMan(position, color=[.8,.8,.8], headsize=[40,40])
	loader = Al(sm)
	loader.attr_setter_type = "as-is"
	isnumber = isnumber
	outdir = "animations"
	if not os.path.exists(outdir):
		os.path.mkdir(outdir)
		
	def __init__(self, *args):
		super().__init__(*args)
		
	def build(self):
		Builder.load_file("main.kv")
		self.theme_cls.theme_style = "Dark"
		#self.theme_cls.primary_palette = "BlueGray"
		main = MainWindow()
		main.add_widget(self.sm)
		return main
		
	def on_pause(self):
		return True
	
	def convertFile(self, file, dest):
		animToXML.convertFile(file, dest)
		
	def register_temp(self, string):
		self.temp_anim_string = string
		self.loader.run(string)
		
	def append_instr(self):
		self.anim_string+=self.temp_anim_string+"\n"

	def reset_stickman(self):
		for attr in dir(self.sm):
			attr = getattr(self.sm, attr)
			if hasattr(attr, "angle"):
				attr.angle = 0
		self.sm.oposition.xy = 0,0
		self.sm.flipped = False
		
	def run_anim(self):
		self.reset_stickman()
		#self.loader.anim_setter_type = "increment"
		print(self.anim_string)
		Clock.schedule_once(lambda dt:self.loader.run(self.anim_string))
		
Editor().run()