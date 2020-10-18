from stickman import StickMan, Circle
from parser.animationloader import Animloader #This one’s for .anim files
from parser.xmlanimparser import Animloader as XAnimloader #And this is for xml files

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color

Window.clearcolor = .2, .5, .7,1
Window.rotation = 0 #set to -90 if you need to rotate the screen to the left by 90 deg
with Window.canvas:
	Color(.3,.3,.3, 1)
	bg = Rectangle(size=[Window.width*4, 40])
	
sm = StickMan((0,0), color=[0]*3)
#Note: To set the bottom of the stickman, that is, where it’s feet touches, set hcenter[1] to (max(headsize)/10)*52 + y
sm.headsize = 40,40
sm.hcenter = 200, 52*4 +40

al = Animloader(sm) #Not needed here
al.attr_setter_type = "as-is" #Also not needed.

alx = XAnimloader(sm)
'''By default, alx.attr_setter_type is set to "as-is" meaning that each sm animation instruction values are always as they are given. Setting it to "increment" causes any new value to be added to the old one.
Example:
------------------
alx = XAnimloader(sm)
alx.attr_setter_type = "increment"
alx.run("""
<StickMan>
	<arm1j1 angle="20"/>
	<arm1j1 angle="40"/> <!--here arm1j1.angle is set to 60 (40+20) since attr_setter_type is "increment"-->
</StickMan>
""")
'''

class TestApp(App):
	def build(self):
		def cb1(e):
			#alx.run_file("animations/backflip_hand.xml")
			alx.run_file("animations/onelegkick.xml")
			def cb2(e):
				#Run the next backflip step
				alx.run_file("animations/walk_full.xml")
				#This next line is necessary to prevent alx.oncomplete from using its current oncomplete callback again (That is, running "animations/walk_step2.xml" again).
				alx.oncomplete = lambda d:print("ended")
			alx.oncomplete = cb2
		alx.oncomplete = cb1
		#Schedules the animation to start after 6 seconds of running this program
		#Clock.schedule_once(lambda dt: alx.run_file("animations/double_punch.xml"), 6)
		#sm.flipped = True
		alx.run('''
		<StickMan>
			<speed speed="2"/>
			<arm1j1 angle="-20"/>
			<uax_rot angle="-5"/>
			<Loop n="4">
				<arm1j2 angle="-120"/>
				<arm1j2 angle="-60"/>
			</Loop>
			<flip/>
		</StickMan>''')
		return sm
		
	def on_pause(self):
		return True

TestApp().run()