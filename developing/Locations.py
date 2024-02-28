import pygame as pyg
import MPlayer as mp
import json
from pygame.locals import *

WORLD = 0
SETTINGS = 1
LOAD = 2
MENU = 3
CREDITS = 4

pyg.font.init()
font_97 = pyg.font.Font("rsrc\\fonts\\times.ttf", 97)
font_48 = pyg.font.Font("rsrc\\fonts\\times.ttf", 48)
font_36 = pyg.font.Font("rsrc\\fonts\\times.ttf", 36)
font_32 = pyg.font.Font("rsrc\\fonts\\times.ttf", 32)
font_24 = pyg.font.Font("rsrc\\fonts\\times.ttf", 24)
font_18 = pyg.font.Font("rsrc\\fonts\\times.ttf", 18)

class Scroller:
	
	def __init__(self, x, y, valueList, index = 0):
		self.x, self.y, self.valueList, self.index = x, y, valueList, index
	
	def update(self):
		mpx, mpy = pyg.mouse.get_pos()[0], pyg.mouse.get_pos()[1]
		if not (mpy >= self.y and mpy <= self.y + 32):
			return
		del mpy
		if mpx < self.x:
			return
		
		if mpx >= self.x and mpx <= self.x + 264:
			#new index
			self.index = self.index + 1 if self.index + 1 < len(self.valueList) else 0
	
	def getElement(self):
		return self.valueList[self.index]
	
	def draw(self, surface):
		pyg.draw.rect(surface, [0, 0, 177], [self.x, self.y, 32 + 32 + 200, 32])
		pyg.draw.rect(surface, [0, 0, 113], [self.x, self.y, 32 + 32 + 200, 32], 2)
		
		blitedText = font_32.render(self.getElement(), 1, [255, 255, 255])
		surface.blit(blitedText, [self.x + 32 + (200 - blitedText.get_width()) / 2, self.y])

class Button:
	
	def __init__(self, x, y, width, height, text):
		self.x, self.y, self.width, self.height, self.clicked = x, y, width, height, False
		self.text = font_32.render(text, 1, [255, 255, 255])
	
	def update(self):
		mpos = pyg.mouse.get_pos()
		if (mpos[0] >= self.x and mpos[0] <= self.x + self.width) and (mpos[1] >= self.y and mpos[1] <= self.y + self.height):
			self.clicked = True
	
	def draw(self, surface):
		pyg.draw.rect(surface, [0, 0, 177], [self.x, self.y, self.width, self.height])
		pyg.draw.rect(surface, [0, 0, 113], [self.x, self.y, self.width, self.height], 2)
		
		surface.blit(self.text, [self.x + (self.width - self.text.get_width()) / 2, self.y])

class SurfButton:
	
	def __init__(self, x, y, width, height, sprite, text = None):
		self.x, self.y, self.width, self.height, self.clicked = x, y, width, height, False
		self.sprite = sprite
		self.text = font_32.render(text, 1, (255, 255, 255)) if text != None else None
	
	def update(self):
		mpos = pyg.mouse.get_pos()
		if (mpos[0] >= self.x and mpos[0] <= self.x + self.width) and (mpos[1] >= self.y and mpos[1] <= self.y + self.height):
			self.clicked = True
	
	def draw(self, surface):
		pyg.draw.rect(surface, [0, 0, 177], [self.x, self.y, self.width, self.height])
		pyg.draw.rect(surface, [0, 0, 113], [self.x, self.y, self.width, self.height], 2)
		
		surface.blit(self.sprite, (self.x, self.y))
		
		if self.text != None:
			surface.blit(self.text, (self.x + (self.width - self.text.get_width()) / 2, self.y))

class ValueChanger:
	
	def __init__(self, x, y, value):
		self.x, self.y, self.value = x, y, value
		self.plus, self.minus = font_32.render("+", 1, [255, 255, 255]), font_32.render("-", 1, [255, 255, 255])
	
	def wcUpdate(self):
		if pyg.mouse.get_pressed()[0]:
			mpos = pyg.mouse.get_pos()
			if (mpos[0] > self.x + 32 and mpos[0] < self.x + 232) and (mpos[1] > self.y and mpos[1] < self.y + 32):
				self.value = int((mpos[0] - 32 - self.x) / 2)
	
	def update(self):
		mx, my = pyg.mouse.get_pos()[0], pyg.mouse.get_pos()[1]
		if (mx >= self.x and mx <= self.x + 32) and (my >= self.y and my <= self.y + 32):
			self.value -= 1 if self.value > 0 else 0
		elif (mx >= self.x + 232 and mx <= self.x + 264) and (my >= self.y and my <= self.y + 32):
			self.value += 1 if self.value < 100 else 0
	
	def draw(self, surface):
		pyg.draw.rect(surface, [0, 0, 177], [self.x, self.y, 32, 32])
		pyg.draw.rect(surface, [0, 0, 113], [self.x, self.y, 32, 32], 2)
		
		pyg.draw.rect(surface, [0, 0, 177], [self.x + 32, self.y, 200, 32])
		pyg.draw.rect(surface, [0, 0, 113], [self.x + 32, self.y, 200, 32], 2)
		
		pyg.draw.rect(surface, [0, 0, 177], [self.x + 232, self.y, 32, 32])
		pyg.draw.rect(surface, [0, 0, 113], [self.x + 232, self.y, 32, 32], 2)
		
		valueText = font_32.render(str(self.value), 1, [255, 255, 255])
		
		surface.blit(self.minus, [self.x + 12, self.y])
		surface.blit(self.plus, [self.x + 244, self.y])
		surface.blit(valueText, [self.x + 32 + ((200 - valueText.get_width()) / 2), self.y + 32])
		
		pyg.draw.rect(surface, [255, 255, 255], [self.x + 32 + self.value * 2, self.y, 2, 32])

class Lever:
	
	def __init__(self, x, y, width, height, on = False):
		self.x, self.y, self.on, self.width, self.height = x, y, on, width, height
		self.yes, self.no = font_36.render(mp.localyze("yes"), 1, [255, 255, 255]), font_36.render(mp.localyze("no"), 1, [255, 255, 255])
	
	def update(self):
		mx, my = pyg.mouse.get_pos()[0], pyg.mouse.get_pos()[1]
		if (mx >= self.x and mx <= self.x + self.width) and (my >= self.y and my <= self.y + self.height):
			self.on = not self.on
	
	def draw(self, surface):
		pyg.draw.rect(surface, [0, 0, 177], [self.x, self.y, self.width, self.height])
		pyg.draw.rect(surface, [0, 0, 113], [self.x, self.y, self.width, self.height], 2)
		surface.blit(self.yes if self.on else self.no, [self.x + self.width / 2 - 25, self.y - 7])

class SettingsLocation:
	
	def __init__(self):
		musicText = font_36.render(mp.localyze("Music Playing"), 1, [255, 255, 255])
		soundText = font_36.render(mp.localyze("Sound Playing"), 1, [255, 255, 255])
		mvt = font_36.render(mp.localyze("Music Volume"), 1, [255, 255, 255])
		svt = font_36.render(mp.localyze("Sound Volume"), 1, [255, 255, 255])
		languageText = font_36.render(mp.localyze("Language"), 1, [255, 255, 255])
		versionText = font_36.render(mp.localyze("Game Version"), 1, [255, 255, 255])
		
		brightnessText = font_36.render(mp.localyze("Brightness"), 1, [255, 255, 255])
		fpsLeverText = font_36.render(mp.localyze("FPS Counter"), 1, [255, 255, 255])
		fpsLimitedText = font_36.render(mp.localyze("is FPS limited"), 1, [255, 255, 255])
		fpsLimiteText = font_36.render(mp.localyze("FPS'S Limite"), 1, [255, 255, 255])
		cursorText = font_36.render(mp.localyze("Cursor"), 1, [255, 255, 255])
		particlesText = font_36.render(mp.localyze("Particles"), 1, [255, 255, 255])
		
		musicVolume = ValueChanger(100, 150, 100)
		soundVolume = ValueChanger(450, 150, 100)
		languageScroller = Scroller(100, 250, ["Russian", "English"], 0)
		musicLever = Lever(100, 50, 256, 32)
		soundLever = Lever(450, 50, 256, 32)
		gameVersion = Lever(450, 250, 256, 32)
		
		brightnessController = ValueChanger(100, 50, 100)
		fpsLever = Lever(450, 150, 256, 32)
		limitedFpsLever = Lever(100, 150, 256, 32)
		fpsLimite = ValueChanger(100, 250, 100)
		cursorScroller = Scroller(450, 250, [mp.localyze("Standart Cursor"), mp.localyze("Big Cursor"), mp.localyze("Small Cursor")])
		particlesScroller = Scroller(450, 50, [mp.localyze("Minimum"), mp.localyze("Medium"), mp.localyze("Maximum")])
		
		jsonLoaded = open("settings.json", mode='r')
		data = json.load(jsonLoaded)
		jsonLoaded.close()
		
		musicLever.on = data["musicOn"]
		soundLever.on = data["soundOn"]
		musicVolume.value = int(data["musicVolume"] * 100)
		soundVolume.value = int(data["soundVolume"] * 100)
		gameVersion.on = data["version"]
		
		brightnessController.value = data["brightness"]
		fpsLever.on = data["fps"]
		limitedFpsLever.on = data["fpslimited"]
		fpsLimite.value = data["fpslimite"]
		particlesScroller.index = data["particles"]
		
		langInData = data["language"]
		if langInData == "English":
			languageScroller.index = 1
		
		cursorInData = data["cursor"]
		if cursorInData in [0, 1, 2]:
			cursorScroller.index = cursorInData
		else:
			raise BaseException()
		
		del data
		
		firstPage = []
		firstPage.append(musicVolume)
		firstPage.append(soundVolume)
		firstPage.append(languageScroller)
		firstPage.append(musicLever)
		firstPage.append(soundLever)
		firstPage.append(gameVersion)
		
		firstPageTexts = []
		firstPageTexts.append((musicText, 100, 14))
		firstPageTexts.append((soundText, 450, 14))
		firstPageTexts.append((mvt, 100, 118))
		firstPageTexts.append((svt, 450, 118))
		firstPageTexts.append((languageText, 100, 214))
		firstPageTexts.append((versionText, 450, 214))
		
		secondPage = []
		secondPage.append(brightnessController)
		secondPage.append(fpsLever)
		secondPage.append(limitedFpsLever)
		secondPage.append(fpsLimite)
		secondPage.append(cursorScroller)
		secondPage.append(particlesScroller)
		
		secondPageTexts = []
		secondPageTexts.append((brightnessText, 100, 14))
		secondPageTexts.append((fpsLeverText, 450, 114))
		secondPageTexts.append((fpsLimitedText, 100, 114))
		secondPageTexts.append((fpsLimiteText, 100, 214))
		secondPageTexts.append((cursorText, 450, 214))
		secondPageTexts.append((particlesText, 450, 14))
		
		self.pages = [firstPage, secondPage]
		self.textPages = [firstPageTexts, secondPageTexts]
		self.pageIndex = 0
		self.pageIndexMin = 0
		self.pageIndexMax = 1
		
		prevButtonSpr = pyg.image.load("rsrc\\sprites\\prevButton.png")
		nextButtonSpr = pyg.transform.flip(prevButtonSpr, True, False)
		self.previousPageButton = SurfButton(49, 500, 224, 48, prevButtonSpr.convert_alpha())
		self.nextPageButton = SurfButton(527, 500, 224, 48, nextButtonSpr.convert_alpha())
		self.saveButton = Button(288, 500, 224, 48, mp.localyze("Save Changes"))
	
	def update(self):
		if self.previousPageButton.clicked:
			self.previousPageButton.clicked = False
			
			if self.pageIndex > self.pageIndexMin:
				self.pageIndex -= 1
		elif self.nextPageButton.clicked:
			self.nextPageButton.clicked = False
			
			if self.pageIndex < self.pageIndexMax:
				self.pageIndex += 1
		elif self.saveButton.clicked:
			self.saveButton.clicked = False
			jsonLoaded = open("settings.json", mode='r')
			data = json.load(jsonLoaded)
			jsonLoaded.close()
			devMo = data["developMode"]
			del data
			del jsonLoaded
			
			data = {}
			data["developMode"] = devMo
			data["musicVolume"] = self.pages[0][0].value / 100
			data["soundVolume"] = self.pages[0][1].value / 100
			data["language"] = self.pages[0][2].getElement()
			data["musicOn"] = self.pages[0][3].on
			data["soundOn"] = self.pages[0][4].on
			data["version"] = self.pages[0][5].on
			
			data["brightness"] = self.pages[1][0].value
			data["fps"] = self.pages[1][1].on
			data["fpslimited"] = self.pages[1][2].on
			data["fpslimite"] = self.pages[1][3].value
			data["cursor"] = self.pages[1][4].index
			data["particles"] = self.pages[1][5].index
			
			jsonLoaded = open("settings.json", mode='w')
			json.dump(data, jsonLoaded, sort_keys = True, indent = 4)
			jsonLoaded.close()
			
			#Go to the main menu
			raise BaseException()
		
		for pageElement in self.pages[self.pageIndex]:
			try:
				pageElement.wcUpdate()
			except AttributeError:
				pass
		
		for event in pyg.event.get():
			if event.type == QUIT:
				raise SystemExit()
			elif event.type == KEYUP and event.key == K_ESCAPE:
				raise BaseException()
			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				self.saveButton.update()
				self.previousPageButton.update()
				self.nextPageButton.update()
				
				for pageElement in self.pages[self.pageIndex]:
					pageElement.update()
	
	def draw(self, surface):
		surface.fill([0, 0, 0])
		
		for pageElement in self.pages[self.pageIndex]:
			pageElement.draw(surface)
		
		for pageText in self.textPages[self.pageIndex]:
			surface.blit(pageText[0], (pageText[1], pageText[2]))
		
		self.saveButton.draw(surface)
		self.previousPageButton.draw(surface)
		self.nextPageButton.draw(surface)
		
		pageNumberStr = str(self.pageIndex + 1) + "/" + str(self.pageIndexMax + 1)
		pageNumber = font_24.render(pageNumberStr, 1, (255, 255, 255))
		surface.blit(pageNumber, (288 + (224 - pageNumber.get_width()) / 2, 563))

class Line:
	
	def __init__(self, text, color, y):
		self.text = font_36.render(text, 1, color)
		self.x, self.y = (800 - self.text.get_width()) / 2, y
	
	def update(self):
		self.y -= 2
	
	def draw(self, surface):
		surface.blit(self.text, (self.x, self.y))

class GameStartLocation:
	
	def __init__(self):
		self.backButton = Button(30, 500, 220, 50, mp.localyze("Back"))
		self.doneButton = Button(530, 500, 220, 50, mp.localyze("Continue"))
		
		self.savenameEntering = ""
		self.seedEntering = ""
		
		self.formLabel = font_36.render(mp.localyze("Enter savename"), 1, (255, 255, 255))
		self.form2Label = font_36.render(mp.localyze("Enter generator seed"), 1, (255, 255, 255))
		
		self.index_focused = 0
	
	def update(self):
		for event in pyg.event.get():
			if event.type == QUIT:
				raise SystemExit()
			elif event.type == MOUSEBUTTONDOWN:
				self.backButton.update()
				self.doneButton.update()
				
				if self.backButton.clicked or self.doneButton.clicked:
					if self.doneButton.clicked:
						if self.seedEntering != "":
							result = 0
							den = 0
							self.seedEntering = list(self.seedEntering)
							self.seedEntering.reverse()
							for element in self.seedEntering:
								result += abs(ord(element[0]) - 48) * 10 ** den
								den += 1
							self.seed = result
							self.seedEntering = ""
						else:
							self.seed = None
					
					raise BaseException()
				else:
					if 230 < event.pos[0] < 230 + 330 and 70 < event.pos[1] < 70 + 40:
						self.index_focused = 0
					elif 230 < event.pos[0] < 230 + 330 and 146 < event.pos[1] < 146 + 40:
						self.index_focused = 1
			elif event.type == KEYDOWN:
				if event.key == K_BACKSPACE:
					if self.index_focused == 0:
						self.savenameEntering = self.savenameEntering[:len(self.savenameEntering) - 1]
					elif self.index_focused == 1:
						self.seedEntering = self.seedEntering[:len(self.seedEntering) - 1]
				elif event.key == K_ESCAPE:
					self.backButton.clicked = True
					raise BaseException()
				elif event.unicode == " " or event.unicode.isdigit() or event.unicode.isalpha():
					if self.index_focused == 0:
						self.savenameEntering += event.unicode
						self.savenameEntering = self.savenameEntering[:14]
					elif self.index_focused == 1:
						self.seedEntering += event.unicode
						self.seedEntering = self.seedEntering[:14]
	
	def draw(self, surface):
		surface.fill((0, 0, 0))
		self.backButton.draw(surface)
		self.doneButton.draw(surface)
		
		pyg.draw.rect(surface, (0, 255, 0) if self.index_focused == 0 else (255, 0, 0), (230, 70, 330, 40), 4)
		pyg.draw.rect(surface, (0, 0, 177), (232, 72, 326, 36))
		
		pyg.draw.rect(surface, (0, 255, 0) if self.index_focused == 1 else (255, 0, 0), (230, 146, 330, 40), 4)
		pyg.draw.rect(surface, (0, 0, 177), (232, 148, 326, 36))
		
		textAboutSavename = font_36.render(self.savenameEntering, 1, (255, 255, 255))
		surface.blit(textAboutSavename, (230, 72))
		
		textAboutSeed = font_36.render(self.seedEntering, 1, (255, 255, 255))
		surface.blit(textAboutSeed, (230, 148))
		
		surface.blit(self.formLabel, (230, 34))
		surface.blit(self.form2Label, (230, 110))

class CreditsLocation:
	
	def __init__(self):
		self.credits = []
		self.credits.append(Line("Game by L. Grigory", [255, 255, 255], 636))
		self.credits.append(Line("L. Grigory as Programmer", [255, 255, 255], 672))
		self.credits.append(Line("L. Grigory as painter", [255, 255, 255], 708))
		self.credits.append(Line("V. Dmitry as painter", [255, 255, 255], 744))
		self.credits.append(Line("L. Grigory as game designer", [255, 255, 255], 780))
		self.credits.append(Line("V. Dmitry as music maker", [255, 255, 255], 816))
		self.credits.append(Line("V. Dmitry as sound maker", [255, 255, 255], 852))
		self.credits.append(Line("Thank you for playing!", [255, 255, 255], 960))
	
	def update(self):
		for event in pyg.event.get():
			if event.type == QUIT:
				raise SystemExit()
			elif event.type == KEYUP and event.key == K_ESCAPE:
				raise BaseException()
		
		for line in self.credits:
			line.update()
		
		for line in self.credits:
			if line.y >= -line.text.get_height():
				break
		else:
			raise BaseException()
	
	def draw(self, surface):
		surface.fill([0, 0, 0])
		for line in self.credits:
			line.draw(surface)

class MenuLocation:
	
	def __init__(self):
		self.loadContent()
		self.goto = WORLD
		self.capslock = False
		jsonLoaded = open("settings.json", 'r')
		data = json.load(jsonLoaded)
		jsonLoaded.close()
		self.isVersionShowed = data["version"]
		del data
	
	def loadContent(self):
		mp.playMusic("firstlocations")
	
	def update(self):
		for event in pyg.event.get():
			if event.type == MOUSEBUTTONUP and event.button == 1:
				if (event.pos[0] >= 375 and event.pos[0] <= 705) and (event.pos[1] >= 340 and event.pos[1] <= 390):
					raise SystemExit()
				elif (event.pos[0] >= 375 and event.pos[0] <= 705) and (event.pos[1] >= 175 and event.pos[1] <= 225):
					raise BaseException()
				elif (event.pos[0] >= 375 and event.pos[0] <= 705) and (event.pos[1] >= 230 and event.pos[1] <= 280):
					self.goto = LOAD
					raise BaseException()
				elif (event.pos[0] >= 375 and event.pos[0] <= 705) and (event.pos[1] >= 285 and event.pos[1] <= 340):
					self.goto = SETTINGS
					raise BaseException()
				elif (event.pos[0] >= 375 and event.pos[0] <= 705) and (event.pos[1] >= 395 and event.pos[1] <= 445):
					self.goto = CREDITS
					raise BaseException()
			elif event.type == QUIT:
				raise SystemExit()
	
	def draw(self, surface):
		surface.fill([0, 0, 0])
		
		logotypeL = font_97.render("L", 1, [255, 0, 0])
		logotypeU = font_97.render("u", 1, [0, 255, 0])
		logotypeS = font_97.render("s", 1, [0, 0, 255])
		logotypeT = font_97.render("t", 1, [255, 255, 0])
		logotypeO = font_97.render("o", 1, [255, 255, 255])
		logotypeX = font_97.render("x", 1, [255, 0, 255])
		
		surface.blit(logotypeL, [285, 25])
		surface.blit(logotypeU, [340, 25])
		surface.blit(logotypeS, [390, 25])
		surface.blit(logotypeT, [430, 25])
		surface.blit(logotypeO, [465, 25])
		surface.blit(logotypeX, [515, 25])
		
		pyg.draw.rect(surface, [0, 0, 177], [375, 175, 330, 50])
		pyg.draw.rect(surface, [0, 0, 177], [375, 230, 330, 50])
		pyg.draw.rect(surface, [0, 0, 177], [375, 285, 330, 50])
		pyg.draw.rect(surface, [0, 0, 177], [375, 340, 330, 50])
		pyg.draw.rect(surface, [0, 0, 177], [375, 395, 330, 50])
		
		pyg.draw.rect(surface, [0, 0, 113], [375, 175, 330, 50], 2)
		pyg.draw.rect(surface, [0, 0, 113], [375, 230, 330, 50], 2)
		pyg.draw.rect(surface, [0, 0, 113], [375, 285, 330, 50], 2)
		pyg.draw.rect(surface, [0, 0, 113], [375, 340, 330, 50], 2)
		pyg.draw.rect(surface, [0, 0, 113], [375, 395, 330, 50], 2)
		
		playText = font_48.render(mp.localyze("New Game"), 1, [255, 255, 255])
		loadText = font_48.render(mp.localyze("Load"), 1, [255, 255, 255])
		settingsText = font_48.render(mp.localyze("Settings"), 1, [255, 255, 255])
		quitText = font_48.render(mp.localyze("Quit The Game"), 1, [255, 255, 255])
		creditsText = font_48.render(mp.localyze("Credits"), 1, [255, 255, 255])
		
		textAboutAuthor = font_24.render(mp.localyze("By L. Grigory"), 1, [255, 255, 255])
		surface.blit(textAboutAuthor, [325, 125])
		
		if self.isVersionShowed:
			ver = "v Pre-Alpha "
			for element in pyg.version.vernum:
				ver += str(element) + "."
			ver = ver[:len(ver) - 1]
			textAboutVersion = font_18.render(ver, 1, [255, 255, 255])
			surface.blit(textAboutVersion, [570, 100])
		
		surface.blit(playText, [375, 175])
		surface.blit(loadText, [375, 230])
		surface.blit(settingsText, [375, 285])
		surface.blit(quitText, [375, 340])
		surface.blit(creditsText, [375, 395])

class GameLoadingLocation:
	
	def __init__(self):
		self.backButton = Button(30, 500, 220, 50, mp.localyze("Back"))
		self.okButton = Button(530, 500, 220, 50, mp.localyze("Continue"))
		
		self.entering = ""
		self.enterText = font_36.render(mp.localyze("Enter savefile name"), 1, (255, 255, 255))
	
	def update(self):
		for event in pyg.event.get():
			if event.type == QUIT:
				raise SystemExit()
			elif event.type == KEYUP and event.key == K_ESCAPE:
				self.backButton.clicked = True
				raise BaseException()
			elif event.type == KEYUP and event.key == K_BACKSPACE:
				self.entering = self.entering[:len(self.entering) - 1]
			elif event.type == KEYDOWN:
				if event.unicode.isdigit() or event.unicode.isalpha() or event.unicode == " ":
					self.entering += event.unicode
					self.entering = self.entering[:14]
			elif event.type == MOUSEBUTTONDOWN:
				self.backButton.update()
				self.okButton.update()
				
				if self.backButton.clicked or self.okButton.clicked:
					raise BaseException()
	
	def draw(self, surface):
		surface.fill((0, 0, 0))
		
		self.backButton.draw(surface)
		self.okButton.draw(surface)
		
		pyg.draw.rect(surface, (0, 255, 0), (230, 70, 330, 40), 4)
		pyg.draw.rect(surface, (0, 0, 177), (232, 72, 326, 36))
		
		surface.blit(font_36.render(self.entering, 1, (255, 255, 255)), (232, 72))
		
		surface.blit(self.enterText, (230, 34))