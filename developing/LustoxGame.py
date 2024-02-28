import pygame as pyg
import MPlayer as mp

import sys
import json
import datetime
from Locations import SettingsLocation, CreditsLocation, MenuLocation, GameStartLocation, GameLoadingLocation, WORLD, SETTINGS, LOAD, MENU, CREDITS
from WorldLocation import *
from GameExceptions import *

from pygame.locals import *

class LustboxGame:
	
	def __init__(self):
		#Cursors: 0-Standart, 1-Big, 2-Small
		
		pyg.init()
		
		mp.GameSounds.initializeGameSounds()
		
		pyg.display.set_caption("Lustox")
		pyg.display.set_icon(pyg.image.load("rsrc\\icons\\icon.ico"))
		self.window = pyg.display.set_mode((800, 600))
		self.clock = pyg.time.Clock()
		self.FPS = 60
		pyg.version.vernum = (0, 1, 8, 0, 1)
		self.location = MenuLocation()
		
		jsonLoaded = open("settings.json", mode = 'r')
		data = json.load(jsonLoaded)
		jsonLoaded.close()
		del jsonLoaded
		
		if data["cursor"] == 0:
			self.cursor = None
			self.cursoroffset = 0
			pyg.mouse.set_visible(True)
		else:
			pyg.mouse.set_visible(False)
			if data["cursor"] == 1:
				self.cursoroffset = 16
				self.cursor = pyg.image.load("rsrc\\icons\\bigcursor.png").convert_alpha()
			elif data["cursor"] == 2:
				self.cursoroffset = 8
				self.cursor = pyg.image.load("rsrc\\icons\\smallcursor.png").convert_alpha()
			else:
				raise BaseException()
		
		bright = (100 - data["brightness"] + 1) * 2
		
		self.showFps = data["fps"]
		self.tempFps = -1
		self.fpsFont = pyg.font.Font("rsrc\\fonts\\fpsfont.ttf", 36)
		
		self.fpsLimite = data["fpslimite"]
		self.isFpsLimited = data["fpslimited"]
		
		del data
		
		self.surf = pyg.Surface((800, 600))
		self.surf.fill((0, 0, 0))
		self.surf.set_alpha(bright)
		
		WorldLocation.locLoad()
	
	def run(self):
		while True:
			self.update()
			self.draw()
			self.clock.tick(10000 if not self.isFpsLimited else self.fpsLimite)
			self.tempFps = self.clock.get_fps()
	
	def update(self):
		try:
			self.location.update()
		except ScreenshotException:
			self.makeScreenshot()
		except SystemExit:
			pyg.quit()
			sys.exit()
		except BaseException as be:
			if type(be) == BaseException:
				self.flipLocation()
			else:
				raise be
	
	def makeScreenshot(self):
		screenName = ""
		now = datetime.datetime.now()
		
		screenName += str(now.year) + "-"
		screenName += str(now.month) + "-"
		screenName += str(now.day) + "_"
		screenName += str(now.hour) + "."
		screenName += str(now.minute) + "."
		screenName += str(now.second)
		
		pyg.image.save(self.window, "screenshots\\" + screenName + ".png")
		
		self.location.player.sendMessage(mp.localyze("The screenshot was saved with the name ") + screenName)
	
	def load(self, enter):
		self.location = WorldLocation()
		self.location.load("saves\\" + enter)
	
	def flipLocation(self):
		if type(self.location) == MenuLocation:
			if self.location.goto == WORLD:
				self.location = GameStartLocation()
			elif self.location.goto == LOAD:
				self.location = GameLoadingLocation()
			elif self.location.goto == SETTINGS:
				self.location = SettingsLocation()
			elif self.location.goto == CREDITS:
				self.location = CreditsLocation()
		elif type(self.location) == WorldLocation:
			self.location = MenuLocation()
			WorldLocation.locRestart()
		elif type(self.location) == CreditsLocation:
			self.location = MenuLocation()
		elif type(self.location) == SettingsLocation:
			#Cursor Changing
			jsonLoaded = open("settings.json", mode = 'r')
			data = json.load(jsonLoaded)
			jsonLoaded.close()
			del jsonLoaded
			
			if data["cursor"] == 0:
				self.cursor = None
				self.cursoroffset = 0
				pyg.mouse.set_visible(True)
			else:
				pyg.mouse.set_visible(False)
				if data["cursor"] == 1:
					self.cursoroffset = 16
					self.cursor = pyg.image.load("rsrc\\icons\\bigcursor.png").convert_alpha()
				elif data["cursor"] == 2:
					self.cursoroffset = 8
					self.cursor = pyg.image.load("rsrc\\icons\\smallcursor.png").convert_alpha()
				else:
					raise BaseException()
			
			self.surf.set_alpha((100 - data["brightness"] + 1) * 2)
			
			self.showFps = data["fps"]
			
			self.fpsLimite = data["fpslimite"]
			self.isFpsLimited = data["fpslimited"]
			
			del data
			
			#Goto menu
			self.location = MenuLocation()
		elif type(self.location) == GameStartLocation:
			if self.location.backButton.clicked:
				self.location = MenuLocation()
			elif self.location.doneButton.clicked:
				gamename = self.location.savenameEntering
				
				if gamename == "" or gamename[0] == " ":
					return
				
				seed = self.location.seed
				self.location = WorldLocation()
				try:
					self.location.generateWorld(seed, self.window)
				except SystemExit:
					pyg.quit()
					sys.exit()
				self.location.gamename = gamename
		elif type(self.location) == GameLoadingLocation:
			if self.location.backButton.clicked:
				self.location = MenuLocation()
			elif self.location.okButton.clicked:
				gamename = self.location.entering
				
				if gamename == "" or gamename[0] == " ":
					return
				
				self.load(self.location.entering)
	
	def draw(self):
		try:
			if type(self.location) == WorldLocation:
				self.location.draw(self.window, self.surf)
			else:
				self.location.draw(self.window)
		except BaseException as be:
			if type(be) == BaseException:
				self.flipLocation()
			else:
				raise be
		
		if self.showFps:
			t_fps = str(int(self.tempFps // 1))
			self.window.blit(self.fpsFont.render(t_fps, 1, [0, 0, 127]), (760, 0))
		
		if self.surf.get_alpha() != 2:
			self.window.blit(self.surf, (0, 0))
		
		if self.cursor != None and pyg.mouse.get_focused():
			mpos = pyg.mouse.get_pos()
			self.window.blit(self.cursor, (mpos[0] - self.cursoroffset, mpos[1] - self.cursoroffset))
		
		#pyg.display.update()
		pyg.display.flip()