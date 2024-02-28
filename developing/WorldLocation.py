import pygame as pyg
import math
import random
import datetime
import json
import sys
import MPlayer as mp
from pygame.locals import *

from PlayerObject import *
from SpriteAnimation import *
from Items import *

from GameExceptions import *
from StaticData import DatabaseStatic

class WorldLocation():
	
	locObjects = []
	locDroppedItems = []
	
	def __init__(self):
		self.width = 5120
		self.height = 5120
		self.player = PlayerObject(2560, 2560)
		self.playerIsDead = False
		self.exitMode = False
		self.controlKeys = [K_w, K_a, K_s, K_d, K_o, K_y, K_i, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0]
		self.controlKeys += [K_q, K_r, K_u, K_p, K_ESCAPE, K_F9, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_PRINT, 13]
		self.controlKeys += [K_F10]
		
		jsonSettings = open("settings.json", mode='r')
		data = json.load(jsonSettings)
		jsonSettings.close()
		self.advanced = data["developMode"]
		
		DatabaseStatic.static_world = self
		DatabaseStatic.static_player = self.player
	
	@staticmethod
	def locRestart():
		WorldLocation.locObjects = []
		WorldLocation.locDroppedItems = []
		WorldLocation.locLoad()
	
	@staticmethod
	def locLoad():
		for i in range(5120 // 32 + 1):
			_l = []
			for j in range(5120 // 32 + 1):
				_l.append(None)
			WorldLocation.locObjects.append(_l)
	
	@staticmethod
	def locAdd(x, y, object):
		x //= 32
		y //= 32
		if not isinstance(object, DroppedItem):
			if -1 < x <= 160 and -1 < y <= 160:
				WorldLocation.locObjects[x][y] = object
		else:
			WorldLocation.locDroppedItems.append(object)
	
	@staticmethod
	def locGet(x, y):
		x //= 32
		y //= 32
		if -1 < x <= 160 and -1 < y <= 160:
			return WorldLocation.locObjects[x][y]
		return None
	
	@staticmethod
	def locGenGet(x, y):
		if -1 < x <= 160 and -1 < y <= 160:
			return WorldLocation.locObjects[x][y]
		return None
	
	@staticmethod
	def locGen(x, y, object):
		if not isinstance(object, DroppedItem):
			if -1 < x <= 160 and -1 < y <= 160:
				WorldLocation.locObjects[x][y] = object
		else:
			WorldLocation.locDroppedItems.append(object)
	
	def genDraw(self, stage, percents, surface, font):
		surface.fill([0, 0, 0])
		
		textAboutStage0 = font.render(stage[0], 1, [255, 255, 255])
		textAboutStage1 = font.render(stage[1], 1, [255, 255, 255])
		textAboutPercents = font.render(str(percents) + "%", 1, [255, 255, 255])
		surface.blit(textAboutStage0, [(800 - textAboutStage0.get_width()) / 2 + 10, 100])
		surface.blit(textAboutStage1, [(800 - textAboutStage1.get_width()) / 2 + 10, 150])
		surface.blit(textAboutPercents, [366, 200])
		
		pyg.draw.ellipse(surface, [0, 0, 255], [118, 400, 64, 64])
		pyg.draw.rect(surface, [0, 0, 255], [150, 400, 500, 64])
		pyg.draw.ellipse(surface, [0, 0, 255], [618, 400, 64, 64])
		pyg.draw.rect(surface, [100, 100, 100], [150, 400, percents * 5, 64])
		
		pyg.display.update()
		
		for event in pyg.event.get():
			if event.type == QUIT:
				raise SystemExit()
	
	def generateWorld(self, seed, surface):
		font = pyg.font.Font("rsrc\\fonts\\times.ttf", 48)
		
		stage, percents = (mp.localyze("First"), mp.localyze("Initializating...")), 0
		self.genDraw(stage, percents, surface, font)
		
		now = datetime.datetime.now()
		self.seed = seed if seed != None else (now.hour * now.minute * now.second + now.microsecond)
		random.seed(self.seed)
		del now
		
		self.oceanX, self.oceanY = random.randint(0, 160), random.randint(0, 160)
		self.desertX, self.desertY = random.randint(0, 160), random.randint(0, 160)
		self.forestX, self.forestY = random.randint(0, 160), random.randint(0, 160)
		
		stage, percents = (mp.localyze("Desert Generation..."), ""), 14
		self.genDraw(stage, percents, surface, font)
		
		for i in range(-16, 17, 1):
			for j in range(-16, 17, 1):
				WorldLocation.locGen(j + self.desertX, i + self.desertY, SandObject(32 * (j + self.desertX), 32 * (i + self.desertY)))
		for i in range(-16, 17, 1):
			if random.choice([True, False]):
				WorldLocation.locGen(i + self.desertX, self.desertY - 17, SandObject(32 * (i + self.desertX), 32 * (self.desertY - 17)))
		for i in range(-16, 17, 1):
			if random.choice([True, False]):
				WorldLocation.locGen(i + self.desertX, self.desertY + 17, SandObject((i + self.desertX) * 32, (self.desertY + 17) * 32))
		for i in range(-16, 17, 1):
			if random.choice([True, False]):
				WorldLocation.locGen(self.desertX - 17, i + self.desertY, SandObject((self.desertX - 17) * 32, (i + self.desertY) * 32))
		for i in range(-16, 17, 1):
			if random.choice([True, False]):
				WorldLocation.locGen(self.desertX + 17, i + self.desertY, SandObject((self.desertX + 17) * 32, (i + self.desertY) * 32))
		
		stage, percents = (mp.localyze("Ocean Generation..."), ""), 28
		self.genDraw(stage, percents, surface, font)
		
		for i in range(-16, 17, 1):
			for j in range(-16, 17, 1):
				if WorldLocation.locGenGet(j + self.oceanX, i + self.oceanY) == None:
					WorldLocation.locGen(j + self.oceanX, i + self.oceanY, WaterObject(32 * (j + self.oceanX), 32 * (i + self.oceanY)))
		for i in range(-16, 17, 1):
			if random.choice([True, False]):
				if WorldLocation.locGenGet(i + self.oceanX, self.oceanY - 17) == None:
					WorldLocation.locGen(i + self.oceanX, self.oceanY - 17, LiquidWaterObject((i + self.oceanX) * 32, (self.oceanY - 17) * 32, random.randint(0, 3), random.choice([True, False])))
		for i in range(-16, 17, 1):
			if random.choice([True, False]):
				if WorldLocation.locGenGet(i + self.oceanX, self.oceanY + 17) == None:
					WorldLocation.locGen(i + self.oceanX, self.oceanY + 17, LiquidWaterObject((i + self.oceanX) * 32, (self.oceanY + 17) * 32, random.randint(0, 3), random.choice([True, False])))
		for i in range(-16, 17, 1):
			if random.choice([True, False]):
				if WorldLocation.locGenGet(self.oceanX - 17, i + self.oceanY) == None:
					WorldLocation.locGen(self.oceanX - 17, i + self.oceanY, LiquidWaterObject((self.oceanX - 17) * 32, (i + self.oceanY) * 32, random.randint(0, 3), random.choice([True, False])))
		for i in range(-16, 17, 1):
			if random.choice([True, False]):
				if WorldLocation.locGenGet(self.oceanX + 17, i + self.oceanY) == None:
					WorldLocation.locGen(self.oceanX + 17, i + self.oceanY, LiquidWaterObject((self.oceanX + 17) * 32, (i + self.oceanY) * 32, random.randint(0, 3), random.choice([True, False])))
		
		stage, percents = (mp.localyze("Forest Generation..."), ""), 42
		self.genDraw(stage, percents, surface, font)
		
		for i in range(67 + random.randint(1, 6)):
			cX, cY = (self.forestX + random.randint(-16, 16)) * 32, (self.forestY + random.randint(-16, 16)) * 32
			if WorldLocation.locGet(cX, cY) == None:
				if random.choice([False, True]):
					WorldLocation.locAdd(cX, cY, TreeObject(cX, cY))
				else:
					WorldLocation.locAdd(cX, cY, BirchObject(cX, cY))
		
		for i in range(random.randint(1, 6)):
			cX, cY = (self.forestX + random.randint(-16, 16)) * 32, (self.forestY + random.randint(-16, 16)) * 32
			if WorldLocation.locGet(cX, cY) == None:
				WorldLocation.locAdd(cX, cY, HoneyBirchObject(cX, cY))
		
		for i in range(67 + random.randint(1, 6)):
			cX, cY = (self.forestX + random.randint(-16, 16)) * 32, (self.forestY + random.randint(-16, 16)) * 32
			if WorldLocation.locGet(cX, cY) == None:
				flowersVariations = [RedFlowerObject, OrangeFlowerObject, BlueFlowerObject, PinkFlowerObject]
				WorldLocation.locAdd(cX, cY, flowersVariations[random.randint(0, 3)](cX, cY))
		
		stage, percents = (mp.localyze("Second"), mp.localyze("Initializating...")), 56
		self.genDraw(stage, percents, surface, font)
		
		watersX, watersY = [], []
		treesX, treesY = [], []
		flowersX, flowersY = [], []
		self.marbleChunkX = random.choice((random.randint(1, 60), random.randint(100, 159)))
		self.marbleChunkY = random.choice((random.randint(1, 60), random.randint(100, 159)))
		self.fX = self.marbleChunkX
		self.fY = self.marbleChunkY
		
		stage, percents = (mp.localyze("Flora Generation"), mp.localyze("Flowers, Waters, Trees!")), 70
		self.genDraw(stage, percents, surface, font)
		
		for i in range(random.randint(12, 17)):
			watersX.append(random.randint(0, 160))
			watersY.append(random.randint(0, 160))
		for i in range(random.randint(171, 197)):
			treesX.append(random.randint(0, 160))
			treesY.append(random.randint(0, 160))
		for i in range(random.randint(342, 394)):
			flowersX.append(random.randint(0, 160))
			flowersY.append(random.randint(0, 160))
		
		#Waters generation
		for i in range(len(watersX)):
			if WorldLocation.locGenGet(watersX[i], watersY[i]) == None:
				WorldLocation.locGen(watersX[i], watersY[i], LiquidWaterObject(watersX[i]*32, watersY[i]*32, random.randint(2, 6), True))
		
		#Trees generation(not in forest)
		for i in range(len(treesX)):
			if WorldLocation.locGenGet(treesX[i], treesY[i]) == None:
				if random.choice([True, False]):
					WorldLocation.locGen(treesX[i], treesY[i], TreeObject(treesX[i] * 32, treesY[i] * 32))
				else:
					WorldLocation.locGen(treesX[i], treesY[i], BirchObject(treesX[i] * 32, treesY[i] * 32))
		
		
		#Flowers generation
		flowersVariations = [RedFlowerObject, OrangeFlowerObject, BlueFlowerObject, PinkFlowerObject]
		
		for i in range(len(flowersX)):
			if WorldLocation.locGenGet(flowersX[i], flowersY[i]) == None:
				WorldLocation.locGen(flowersX[i], flowersY[i], flowersVariations[random.randint(0, 3)](flowersX[i] * 32, flowersY[i] * 32))
		
		del flowersVariations
		
		#Stone generation
		
		#mmic is variable what mean was be generated mystery stone
		mmic = False
		
		stage, percents = (mp.localyze("Ruins Generation..."), ""), 84
		self.genDraw(stage, percents, surface, font)
		
		i, j = 0, 0
		for i in range(random.randint(1, 3) + 11):
			for j in range(random.randint(1, 5) + 11):
				xx, yy = self.marbleChunkX + i, self.marbleChunkY + j
				if random.choice([False, True]):
					if WorldLocation.locGenGet(xx, yy) == None:
						WorldLocation.locGen(xx, yy, MarbleObject(xx * 32, yy * 32))
				elif not mmic:
					mmic = True
					WorldLocation.locGen(xx, yy, MysteryStoneObject(xx * 32, yy * 32))
		
		del mmic
		
		self.fX, self.fY = self.marbleChunkX + (j//2) + 1, self.marbleChunkY + (i//2) + 1 
		for xxxx in range(self.fX-2, self.fX+3, 1):
			for yyyy in range(self.fY-2, self.fY+3, 1):
				WorldLocation.locGen(xxxx, yyyy, MarbleObject(xxxx*32, yyyy*32))
		WorldLocation.locGen(self.fX, self.fY, MysteryFlowerObject(self.fX*32, self.fY*32))
		
		stage, percents = (mp.localyze("Cacti Generation..."), ""), 98
		self.genDraw(stage, percents, surface, font)
		
		for i in range(6 + random.randint(1, 13)):
			cX, cY = (self.desertX + random.randint(-16, 16)) * 32, (self.desertY + random.randint(-16, 16)) * 32
			if type(WorldLocation.locGet(cX, cY)) == SandObject:
				WorldLocation.locGet(cX, cY).setOn(CactusObject(cX, cY))
		
		for xxx in range(-7, 7, 1):
			for yyy in range(-7, 7, 1):
				obj = WorldLocation.locGenGet(80 + xxx, 80 + yyy)
				if obj != None and obj.solid:
					WorldLocation.locGen(80 + xxx, 80 + yyy, None)
		
		mp.stopMusic()
	
	def update(self):
		onBlock = None
		mouseClicked = False
		clickPosition = None
		rightButton = False
		
		self.player.update(None)
		
		if self.player.isDead:
			self.playerIsDead = True
		
		for event in pyg.event.get():
			if event.type == QUIT:
				raise SystemExit()
			elif (event.type == KEYUP or event.type == KEYDOWN) and event.key in self.controlKeys:
				if event.key in [K_o, K_y]:
					if self.advanced:
						self.player.update(event)
				elif event.key == K_r and self.advanced:
					fo = WorldLocation.locGenGet(1, 1)
					if fo != None:
						self.player.sendMessage(str(sys.getsizeof(fo)))
					else:
						self.player.sendMessage("undefined object to cell with coord (1, 1)")
				elif event.key == K_u and self.advanced:
					self.player.hp = self.player.maxHp
					self.player.mana = self.player.maxMana
				elif event.key == K_p and self.advanced:
					mess = ("fx:" + str(self.forestX * 32))
					mess += ("fy:" + str(self.forestY * 32))
					mess += ("dx:" + str(self.desertX * 32))
					mess += ("dy:" + str(self.desertY * 32))
					mess += ("cx:" + str(self.oceanX * 32))
					mess += ("cy:" + str(self.oceanY * 32))
					mess += ("mfx:" + str(self.fX * 32))
					mess += ("mfy:" + str(self.fY * 32))
					mess += ("mx:" + str(self.marbleChunkX * 32))
					mess += ("my:" + str(self.marbleChunkY * 32))
					
					self.player.sendMessage(mess)
				elif event.type == KEYUP and event.key == K_F9:
					self.player.sendMessage(str(self.player.moveSpeed))
				elif event.type == KEYUP and event.key == K_F10:
					if self.advanced:
						if self.player.inventory.isWorkbenchOpened:
							self.player.inventory.station.developCraft()
						else:
							self.player.effectManager.clearEffects()
				elif event.type == KEYUP and event.key == 13:
					if self.player.inventory.isWorkbenchOpened:
						self.player.inventory.station.enter()
				elif event.type == KEYUP and event.key == K_ESCAPE:
					self.exitMode = True
					return
				elif event.type == KEYUP and event.key == K_PRINT:
					#print("screen")
					raise ScreenshotException()
				else:
					self.player.update(event)
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					if (event.pos[0] >= 540 and event.pos[0] <= 572) and (event.pos[1] >= 30 and event.pos[1] <= 62):
						self.player.sendMessage(mp.localyze("Seed of the world: ") + str(self.seed))
					elif (event.pos[0] >= 522 and event.pos[0] <= 572) and (event.pos[1] >= 65 and event.pos[1] <= 95):
						self.save()
					else:
						self.player.update(event)
				else:
					self.player.update(event)
			elif event.type == MOUSEBUTTONUP and event.button == 3:
				rightButton = True
				clickPosition = pyg.mouse.get_pos()
		
		if pyg.key.get_pressed()[K_w] or pyg.key.get_pressed()[K_UP]:
			self.player.yPrevious = self.player.y
			self.player.update("up")
		elif pyg.key.get_pressed()[K_s] or pyg.key.get_pressed()[K_DOWN]:
			self.player.yPrevious = self.player.y
			self.player.update("down")
		if pyg.key.get_pressed()[K_a] or pyg.key.get_pressed()[K_LEFT]:
			self.player.xPrevious = self.player.x
			self.player.update("left")
		elif pyg.key.get_pressed()[K_d] or pyg.key.get_pressed()[K_RIGHT]:
			self.player.xPrevious = self.player.x
			self.player.update("right")
		
		if pyg.mouse.get_focused() and pyg.mouse.get_pressed()[0] == 1:
			mouseClicked = True
			clickPosition = pyg.mouse.get_pos()
			onBlock = False
		
		#Dropped items on map objects cycle
		for i in range(len(WorldLocation.locDroppedItems)):
			
			if WorldLocation.locDroppedItems[i].relOutOfScreen(self.player.x, self.player.y):
				continue
			
			#Pickup dropped item by player
			if self.checkColl(self.player.x, self.player.y, WorldLocation.locDroppedItems[i].x, WorldLocation.locDroppedItems[i].y):
				self.player.collisionEvent(WorldLocation.locDroppedItems[i])
				WorldLocation.locDroppedItems[i] = None
		
		#Nonanle dropped items cleaning
		while None in WorldLocation.locDroppedItems:
			WorldLocation.locDroppedItems.remove(None)
		
		#Map objects cycle
		for xx in range(-15, 16):
			for yy in range(-12, 13):
				obj = WorldLocation.locGenGet((self.player.x // 32) + xx, (self.player.y // 32) + yy)
				if obj != None and (not obj.relOutOfScreen(self.player.x, self.player.y)):
					obj.update()
					
					if rightButton:
						#Object Using
						xW = (self.scr("x", clickPosition[0]) // 32) * 32 == obj.x
						yW = (self.scr("y", clickPosition[1]) // 32) * 32 == obj.y
						if xW and yW:
							self.player.objectUsing(obj)
							rightButton = False
					
					#Updating player stats with collisions checking
					if self.checkCollP(self.player.x, self.player.y, obj.x, obj.y):
						self.player.collisionEvent(obj)
					
					#Destroying objects
					if mouseClicked:
						if self.checkCollMS(self.scr("x", clickPosition[0]), self.scr("y", clickPosition[1]), obj.x, obj.y):
							added = self.player.eventClickOn(obj)
							onBlock = True
					
					if self.playerIsDead:
						obj.afterPlayerDiengUpdate()
		
		#Putting blocks to the world
		if onBlock == False:
			cp = (self.scr("x", clickPosition[0]), self.scr("y", clickPosition[1]))
			blockToAdding = self.player.clickOnScreen(cp[0], cp[1])
			if blockToAdding != None:
				WorldLocation.locAdd(blockToAdding.x, blockToAdding.y, blockToAdding)
	
	def save(self):
		savefilename = str(self.gamename)
		self.player.sendMessage(mp.localyze("Saved to folder with the name: ") + savefilename)
		#saving
	
	def load(self, folderName):
		self.seed = -3
		mp.stopMusic()
	
	def scr(self, type, value):
		if type == "x":
			return value + self.player.x - 400
		return value + self.player.y - 300
	
	#Checking any collision and second object is underer and lefter than first object(Diving matrix on cells)
	def checkCollMS(self, x1, y1, x2, y2):
		return self.checkColl(x1, y1, x2, y2) and x1 > x2 and y1 > y2
	
	#Checking any collision, returns true if there is collision else false
	def checkColl(self, x1, y1, x2, y2):
		xCollisions = abs(x2 - x1) < 32
		yCollisions = abs(y2 - y1) < 32
		return xCollisions and yCollisions
	
	#Checking any collision with object and player
	def checkCollP(self, x1, y1, x2, y2):
		xCollisions = abs(x2 - x1) < 25
		yCollisions = abs(y2 - y1) < 25
		return xCollisions and yCollisions
	
	def draw(self, surface, bright):
		#Background Drawing
		
		if self.player.x < 401 or self.player.y < 301 or self.player.x > 4719 or self.player.y > 4819:
			surface.fill([10, 0, 35])
			img_star = pyg.image.load("rsrc\\sprites\\star.png").convert_alpha()
			#img_star = pyg.transform.scale(img_star, (img_star.get_width() - self.offsetX*2, img_star.get_width() - self.offsetY*2))
			
			stars = []
			stars.append((55, 30))
			stars.append((225, 35))
			stars.append((400, 50))
			stars.append((700, 60))
			stars.append((160, 100))
			stars.append((670, 110))
			stars.append((310, 130))
			stars.append((765, 215))
			stars.append((260, 230))
			stars.append((650, 240))
			stars.append((510, 260))
			stars.append((100, 300))
			stars.append((410, 310))
			stars.append((600, 365))
			stars.append((330, 370 ))
			stars.append((210, 380))
			stars.append((660, 430))
			stars.append((500, 450))
			stars.append((650, 500))
			stars.append((55, 510))
			stars.append((430, 530))
			stars.append((760, 555))
			stars.append((230, 585))
			stars.append((785, 365))
			
			for star in stars:
				surface.blit(img_star, (star[0] - (self.player.x/37.5), star[1] - (self.player.y/37.5)))
			
			pyg.draw.rect(surface, [0, 135, 0], [0 - self.player.x + 400, 0 - self.player.y + 300, 5120 + 32, 5120 + 32])
		else:
			surface.fill([0, 135, 0])
		
		#Objects Drawing
		
		for xx in range(-15, 16):
			for yy in range(-12, 13):
				obj = WorldLocation.locGenGet((self.player.x // 32) + xx, (self.player.y // 32) + yy)
				if obj != None and (not obj.relOutOfScreen(self.player.x, self.player.y)):
					obj.drawXY(surface, self.player.x, self.player.y)
		
		#Dropped Items Drawing
		
		for o in WorldLocation.locDroppedItems:
			if not o.relOutOfScreen(self.player.x, self.player.y):
				o.drawXY(surface, self.player.x, self.player.y)
		
		#Player Drawing and Interface Drawing
		
		mousePosition = pyg.mouse.get_pos()
		self.player.draw(surface, mousePosition[0], mousePosition[1])
		
		#Border Drawing
		
		if self.player.x < 401 or self.player.x > 4719 or self.player.y < 301 or self.player.y > 4819:
			pyg.draw.rect(surface, [255, 0, 0], [0 - self.player.x + 400, 0 - self.player.y + 300, 5152, 5152], 5)
		
		# Death Screen Drawing
		
		if self.playerIsDead:
			self.playerIsDead = False
			timeCount = 0
			surface.blit(bright, [0, 0])
			
			bright2 = pyg.Surface((800, 600))
			bright2.fill((0, 0, 0))
			bright2.set_alpha(2)
			
			while True:
				timeCount += 1
				if timeCount == 300:
					break
				for event in pyg.event.get():
					if event.type == QUIT:
						raise SystemExit()
					elif event.type == KEYUP and event.key == K_INSERT:
						screenName = ""
						now = datetime.datetime.now()
						
						screenName += str(now.year) + "-"
						screenName += str(now.month) + "-"
						screenName += str(now.day) + "_"
						screenName += str(now.hour) + "."
						screenName += str(now.minute) + "."
						screenName += str(now.second)
						
						pyg.image.save(surface, "screenshots\\" + screenName + ".png")
						
						self.player.sendMessage(mp.localyze("The screenshot was saved with the name ") + screenName)
				
				surface.blit(bright2, (0, 0))
				
				pyg.display.update()
				
				pyg.time.delay(10)
			
			toExit = False
			for i in range(-3, 4, 1):
				for j in range(-3, 4, 1):
					xx, yy = (self.player.x // 32) + i, (self.player.y // 32) + j
					if WorldLocation.locGenGet(xx, yy) == None:
						if 0 < xx < 159 and 0 < yy < 159:
							otp = CoffinObject(xx * 32, yy * 32)
							WorldLocation.locGen(xx, yy, otp)
							toExit = True
							break				
				if toExit:
					break
			del toExit
			
			self.player.respawn()
		elif self.exitMode:
			self.exitMode = False
			font_24 = pyg.font.Font("rsrc\\fonts\\times.ttf", 24)
			font_28 = pyg.font.Font("rsrc\\fonts\\times.ttf", 28)
			yesTex = font_24.render(mp.localyze("yes"), 1, (255, 255, 255))
			noTex = font_24.render(mp.localyze("no"), 1, (255, 255, 255))
			questionTex = font_28.render(mp.localyze("Do you really want to quit the game?"), 1, (255, 255, 255))
			tipTex = font_28.render(mp.localyze("Your game will be saved."), 1, (255, 255, 255))
			surface.fill((0, 0, 0))
			del font_24
			del font_28
			
			jsonLoaded = open("settings.json", mode = 'r')
			data = json.load(jsonLoaded)
			jsonLoaded.close()
			
			if data["cursor"] == 0:
				self.cursor = None
				self.cursoroffset = 0
			else:
				if data["cursor"] == 1:
					self.cursoroffset = 16
					self.cursor = pyg.image.load("rsrc\\icons\\bigcursor.png").convert_alpha()
				else:
					self.cursoroffset = 8
					self.cursor = pyg.image.load("rsrc\\icons\\smallcursor.png").convert_alpha()
			
			brightness = (100 - data["brightness"] + 1) * 2
			
			del jsonLoaded
			del data
			
			bright = pyg.Surface((800, 600))
			bright.fill((0, 0, 0))
			bright.set_alpha(brightness)
			
			while True:
				surface.fill((0, 0, 0))
				
				for event in pyg.event.get():
					if event.type == QUIT:
						raise SystemExit()
					elif event.type == MOUSEBUTTONDOWN:
						if 200 <= event.pos[0] <= 200 + 75 and 318 <= event.pos[1] <= 318 + 25:
							self.save()
							raise BaseException()
						elif 525 <= event.pos[0] <= 525 + 75 and 318 <= event.pos[1] <= 318 + 25:
							return
				
				pyg.draw.rect(surface, (0, 0, 177), (150, 225, 500, 150))
				pyg.draw.rect(surface, (0, 0, 93), (150, 225, 500, 150), 4)
				pyg.draw.rect(surface, (0, 93, 255), (200, 318, 75, 25))
				pyg.draw.rect(surface, (0, 93, 93), (200, 318, 75, 25), 4)
				pyg.draw.rect(surface, (0, 93, 255), (525, 318, 75, 25))
				pyg.draw.rect(surface, (0, 93, 93), (525, 318, 75, 25), 4)
				surface.blit(yesTex, ((75 - yesTex.get_width()) / 2 + 200, (25 - yesTex.get_height()) / 2 + 318))
				surface.blit(noTex, ((75 - noTex.get_width()) / 2 + 525, (25 - noTex.get_height()) / 2 + 318))
				surface.blit(questionTex, (155, 230))
				surface.blit(tipTex, (155, 258))
				
				if self.cursor != None and pyg.mouse.get_focused():
					mpos = pyg.mouse.get_pos()
					surface.blit(self.cursor, (mpos[0] - self.cursoroffset, mpos[1] - self.cursoroffset))
				
				if brightness != 2:
					surface.blit(bright, (0, 0))
				
				pyg.display.update()