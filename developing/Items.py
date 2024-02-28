import pygame as pyg
import MPlayer as mp
import datetime
import random

from StaticData import DatabaseStatic
from Effects import *
from SpriteAnimation import *

s_poHorizontalWaterSpray1 = pyg.image.load("rsrc\\particles\\waterspray1.png")
s_poHorizontalWaterSpray2 = pyg.image.load("rsrc\\particles\\waterspray2.png")
poHorizontalWaterSpray = SpriteAnimation((s_poHorizontalWaterSpray1, s_poHorizontalWaterSpray2), 2, 60)

poVerticalWaterSpray = rotateAnim(poHorizontalWaterSpray, 90)
poDiagonalWaterSpray1 = rotateAnim(poHorizontalWaterSpray, 225)
poDiagonalWaterSpray2 = rotateAnim(poHorizontalWaterSpray, 315)

class WaterSpray:
	
	def __init__(self, x, y, direct, lifeTimeFrames):
		self.x, self.y, self.direct, self.lifeTimeFrames = x, y, direct, lifeTimeFrames
		self.speed = 0.75
		if self.direct[0] != 0 and self.direct[1] == 0:
			self.surf = poHorizontalWaterSpray
		elif self.direct[1] != 0 and self.direct[0] == 0:
			self.surf = poVerticalWaterSpray
		elif self.direct == (-1, -1) or self.direct == (1, 1):
			self.surf = poDiagonalWaterSpray1
		elif self.direct == (-1, 1) or self.direct == (1, -1):
			self.surf = poDiagonalWaterSpray2
	
	def update(self):
		if self.lifeTimeFrames > 0:
			self.lifeTimeFrames -= 1
			self.x, self.y = self.direct[0] * self.speed + self.x, self.direct[1] * self.speed + self.y
		if not isinstance(DatabaseStatic.static_world.locGet(int(self.x), int(self.y)), WaterObject):
			self.lifeTimeFrames = 0
		elif not isinstance(DatabaseStatic.static_world.locGenGet(int((self.x // 32) + self.direct[0]), int((self.y // 32) + self.direct[1])), WaterObject):
			self.lifeTimeFrames = 0
	
	def draw(self, surface, playerX, playerY):
		surface.blit(self.surf.getSprite(), (int(self.x - playerX + 400), int(self.y - playerY + 300)))

iSpritesDir = "rsrc\\sprites\\"
iSpritesExt = ".png"

iAcornSprite = pyg.image.load(iSpritesDir + "acorn" + iSpritesExt)
iAppleSprite = pyg.image.load(iSpritesDir + "apple" + iSpritesExt)
iDroppedcactusSprite = pyg.image.load(iSpritesDir + "droppedcactus" + iSpritesExt)
iDroppedmarbleSprite = pyg.image.load(iSpritesDir + "droppedmarble" + iSpritesExt)
iDroppedmysteryflowerSprite = pyg.image.load(iSpritesDir + "dmysteryflower" + iSpritesExt)
iDroppedmysterystoneSprite = pyg.image.load(iSpritesDir + "droppedmysterystone" + iSpritesExt)
iDroppedsandSprite = pyg.image.load(iSpritesDir + "droppedsand" + iSpritesExt)
iDroppedwoodSprite = pyg.image.load(iSpritesDir + "droppedwood" + iSpritesExt)
iDroppedworkbenchSprite = pyg.image.load(iSpritesDir + "droppedworkbench" + iSpritesExt)
iWoodenswordSprite = pyg.image.load(iSpritesDir + "woodensword" + iSpritesExt)
iWoodenaxeSprite = pyg.image.load(iSpritesDir + "woodenaxe" + iSpritesExt)
iWoodenpickaxeSprite = pyg.image.load(iSpritesDir + "woodenpickaxe" + iSpritesExt)
iBirchWoodItemSprite = pyg.image.load(iSpritesDir + "droppedbirchwood" + iSpritesExt)
iBirchSaplingItemSprite = pyg.image.load(iSpritesDir + "birchsapling" + iSpritesExt)

iHoney = pyg.image.load(iSpritesDir + "honey" + iSpritesExt)

iAFlowerSprites = [pyg.image.load(iSpritesDir + "dflower" + iSpritesExt), 
				pyg.image.load(iSpritesDir + "dorangeflower" + iSpritesExt), 
				pyg.image.load(iSpritesDir + "dblueflower" + iSpritesExt), 
				pyg.image.load(iSpritesDir + "dpinkflower" + iSpritesExt)]

del iSpritesDir
del iSpritesExt

diSpritesDir = "rsrc\\sprites\\"
diSpritesExt = ".png"

dAcornSprite = pyg.image.load(diSpritesDir + "acorn" + diSpritesExt)
dAppleSprite = pyg.image.load(diSpritesDir + "apple" + diSpritesExt)
dDroppedcactusSprite = pyg.image.load(diSpritesDir + "droppedcactus" + diSpritesExt)
dDroppedmarbleSprite = pyg.image.load(diSpritesDir + "droppedmarble" + diSpritesExt)
dDroppedmysteryflowerSprite = pyg.image.load(diSpritesDir + "dmysteryflower" + diSpritesExt)
dDroppedmysterystoneSprite = pyg.image.load(diSpritesDir + "droppedmysterystone" + diSpritesExt)
dDroppedsandSprite = pyg.image.load(diSpritesDir + "droppedsand" + diSpritesExt)
dDroppedwoodSprite = pyg.image.load(diSpritesDir + "droppedwood" + diSpritesExt)
dDroppedworkbenchSprite = pyg.image.load(diSpritesDir + "droppedworkbench" + diSpritesExt)
dWoodenswordSprite = pyg.image.load(diSpritesDir + "woodensword" + diSpritesExt)
dWoodenaxeSprite = pyg.image.load(diSpritesDir + "woodenaxe" + diSpritesExt)
dWoodenpickaxeSprite = pyg.image.load(diSpritesDir + "woodenpickaxe" + diSpritesExt)
dDroppedBirchWoodSprite = pyg.image.load(diSpritesDir + "droppedbirchwood" + diSpritesExt)
dDroppedBirchSaplingSprite = pyg.image.load(diSpritesDir + "birchsapling" + diSpritesExt)

diAFlowerSprites = [pyg.image.load(diSpritesDir + "dflower" + diSpritesExt),
					pyg.image.load(diSpritesDir + "dorangeflower" + diSpritesExt),
					pyg.image.load(diSpritesDir + "dblueflower" + diSpritesExt),
					pyg.image.load(diSpritesDir + "dpinkflower" + diSpritesExt)]

del diSpritesDir
del diSpritesExt

spritesDir = "rsrc\\sprites\\"
spritesExt = ".png"

crack1Sprite = pyg.image.load(spritesDir + "crack1" + spritesExt)
crack2Sprite = pyg.image.load(spritesDir + "crack2" + spritesExt)
crack3Sprite = pyg.image.load(spritesDir + "crack3" + spritesExt)
crack4Sprite = pyg.image.load(spritesDir + "crack4" + spritesExt)
damages = [None, crack1Sprite, crack2Sprite, crack3Sprite, crack4Sprite]

cactusSprite = pyg.image.load(spritesDir + "cactus" + spritesExt)
marbleSprite = pyg.image.load(spritesDir + "marble" + spritesExt)
mysteryFlowerSprite = pyg.image.load(spritesDir + "mysteryflower" + spritesExt)
mysteryStoneSprite = pyg.image.load(spritesDir + "mysterystone" + spritesExt)
woodPlankSprite = pyg.image.load(spritesDir + "woodplank" + spritesExt)
birchWoodPlankSprite = pyg.image.load(spritesDir + "birchwoodplank" + spritesExt)
workbenchSprite = pyg.image.load(spritesDir + "workbench" + spritesExt)
tableSprite = pyg.image.load(spritesDir + "table" + spritesExt)
birchtableSprite = pyg.image.load(spritesDir + "birchtable" + spritesExt)
cactustableSprite = pyg.image.load(spritesDir + "cactustable" + spritesExt)
clearcactusSprite = pyg.image.load(spritesDir + "clearcactus" + spritesExt)
clearcactustableSprite = pyg.image.load(spritesDir + "clearcactustable" + spritesExt)
leftchairSprite = pyg.image.load(spritesDir + "chairleft" + spritesExt)
rightchairSprite = pyg.image.load(spritesDir + "chairright" + spritesExt)
leftbirchchair = pyg.image.load(spritesDir + "birchchairleft" + spritesExt)
rightbirchchair = pyg.image.load(spritesDir + "birchchairright" + spritesExt)
leftcactuschair = pyg.image.load(spritesDir + "cactuschairleft" + spritesExt)
rightcactuschair = pyg.image.load(spritesDir + "cactuschairright" + spritesExt)
leftclearcactuschair = pyg.image.load(spritesDir + "clearcactuschairleft" + spritesExt)
rightclearcactuschair = pyg.image.load(spritesDir + "clearcactuschairright" + spritesExt)
coffinSprite = pyg.image.load(spritesDir + "coffin" + spritesExt)
woodlinoleumSprite = pyg.image.load(spritesDir + "woodlinoleum" + spritesExt)
birchlinoleumSprite = pyg.image.load(spritesDir + "birchlinoleum" + spritesExt)
cactuslinoleumSprite = pyg.image.load(spritesDir + "cactuslinoleum" + spritesExt)
clearcactuslinoleumSprite = pyg.image.load(spritesDir + "clearcactuslinoleum" + spritesExt)
wooddoorcloseSprite = pyg.image.load(spritesDir + "doorclose" + spritesExt)
wooddooropenSprite = pyg.image.load(spritesDir + "dooropen" + spritesExt)
birchdoorcloseSprite = pyg.image.load(spritesDir + "birchdooropen" + spritesExt)
birchdooropenSprite = pyg.image.load(spritesDir + "birchdoorclose" + spritesExt)
cactusdoorcloseSprite = pyg.image.load(spritesDir + "cactusdoorclose" + spritesExt)
cactusdooropenSprite = pyg.image.load(spritesDir + "cactusdooropen" + spritesExt)
clearcactusdoorcloseSprite = pyg.image.load(spritesDir + "clearcactusdoorclose" + spritesExt)
clearcactusdooropenSprite = pyg.image.load(spritesDir + "clearcactusdooropen" + spritesExt)
woodchestSprite = pyg.image.load(spritesDir + "woodchest" + spritesExt)
birchchestSprite = pyg.image.load(spritesDir + "birchchest" + spritesExt)
cactuschestSprite = pyg.image.load(spritesDir + "cactuschest" + spritesExt)
clearcactuschestSprite = pyg.image.load(spritesDir + "clearcactuschest" + spritesExt)

honeybirchSprite = pyg.image.load(spritesDir + "honey" + spritesExt)

birchworkbenchSprite = pyg.image.load(spritesDir + "birchworkbench" + spritesExt)

playerSits = [GameSprite(pyg.image.load(spritesDir + "playersitleft" + spritesExt)), 
			GameSprite(pyg.image.load(spritesDir + "playersitright" + spritesExt))]

flowersSprites = [pyg.image.load(spritesDir + "flower" + spritesExt), 
				pyg.image.load(spritesDir + "orangeflower" + spritesExt), 
				pyg.image.load(spritesDir + "blueflower" + spritesExt), 
				pyg.image.load(spritesDir + "pinkflower" + spritesExt)]

treesSprites = [pyg.image.load(spritesDir + "tree" + spritesExt), 
				pyg.image.load(spritesDir + "birch" + spritesExt)]

cactusGrows = [pyg.image.load(spritesDir + "cactusgrow1" + spritesExt), 
			pyg.image.load(spritesDir + "cactusgrow2" + spritesExt), 
			pyg.image.load(spritesDir + "cactusgrow3" + spritesExt), 
			pyg.image.load(spritesDir + "cactusgrow4" + spritesExt)]

treeGrows = [pyg.image.load(spritesDir + "treesapling1" + spritesExt), 
			pyg.image.load(spritesDir + "treesapling2" + spritesExt), 
			pyg.image.load(spritesDir + "treesapling3" + spritesExt), 
			pyg.image.load(spritesDir + "treesapling4" + spritesExt)]

birchGrows = [pyg.image.load(spritesDir + "birchgrow1" + spritesExt), 
			pyg.image.load(spritesDir + "birchgrow2" + spritesExt), 
			pyg.image.load(spritesDir + "birchgrow3" + spritesExt), 
			pyg.image.load(spritesDir + "birchgrow4" + spritesExt)]

beehivebirchSprite = pyg.image.load(spritesDir + "honeyBirch0" + spritesExt)

honeyAnimFrames = []
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch0" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch1" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch2" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch3" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch4" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch5" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch6" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch7" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch8" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch9" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch10" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch11" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch12" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch13" + spritesExt))
honeyAnimFrames.append(pyg.image.load(spritesDir + "honeyBirch14" + spritesExt))

honeyAnimation = SpriteAnimation(honeyAnimFrames, 15, 1)

del honeyAnimFrames

del spritesDir
del spritesExt

class Recipe:
	
	def __init__(self, items, result):
		self.items = items
		self.possibility = False
		self.result = result
		self.sprite = result.getSprite()
	
	def repossible(self, storageSection, accessPanel):
		if storageSection == None or accessPanel == None:
			self.possibility = False
			return
		
		copyItems = list(self.items)
		for i in range(len(copyItems)):
			fc = storageSection.getItemCount(copyItems[i])
			fc += accessPanel.getItemCount(copyItems[i])
			if fc >= copyItems[i].count:
				pass
			else:
				self.possibility = False
				return
		self.possibility = True
	
	def craft(self, storageSection, accessPanel):
		copyItems = list(self.items)
		for i in range(len(copyItems)):
			fc = storageSection.dropItems(copyItems[i])
			if fc == 0:
				continue
			accessPanel.dropItems(copyItems[i])
	
	def draw(self, x, y, surface):
		pyg.draw.rect(surface, (25, 25, 255), (x, y, 32, 32))
		pyg.draw.rect(surface, (0, 0, 127), (x, y, 32, 32), 2)
		surface.blit(self.sprite, (x, y))
	
	def drawAsSelected(self, x, y, surface):
		pyg.draw.rect(surface, (25, 25, 255), (x, y, 32, 32))
		pyg.draw.rect(surface, (255, 255, 0), (x, y, 32, 32), 2)
		surface.blit(self.sprite, (x, y))
		
		text = pyg.font.Font("rsrc\\fonts\\times.ttf", 19).render(str(self.result.count), 1, (255, 255, 255))
		
		surface.blit(text, (x, y))
	
	def drawItem(self, surface, x, y, index):
		pyg.draw.rect(surface, (25, 25, 255), (x, y, 32, 32))
		pyg.draw.rect(surface, (0, 0, 127), (x, y, 32, 32), 2)
		surface.blit(self.items[index].getSprite(), (x, y))
		
		text = pyg.font.Font("rsrc\\fonts\\times.ttf", 14).render(str(self.items[index].count), 1, (255, 255, 255))
		
		surface.blit(text, (x, y))
	
	def drawName(self, x, y, surface):
		text = pyg.font.Font("rsrc\\fonts\\times.ttf", 14).render(self.result.itemName, 1, (255, 255, 255))
		surface.blit(text, (x, y))

class Item:
	
	def __init__(self, count = 1):
		self.sprite = None
		self.systemName = ""
		self.count = count
		self.itemName = ""
		self.titles = []
	
	def ini(self):
		self.putObject = None
		self.usableItem = False
	
	def useItem(self):
		pass
	
	def getSingleComponent(self):
		return None
	
	def getInDropped(self):
		return None
	
	def getSprite(self):
		return None
	
	def drawTitles(self, x, y, surface):
		x += 5
		font = pyg.font.Font("rsrc\\fonts\\times.ttf", 20)
		surface.blit(font.render(self.itemName, 1, [255, 255, 255]), [x, y])
		y += 16
		for title in self.titles:
			surface.blit(font.render(title, 1, [255, 255, 255]), [x, y])
			y += 16

class GameObject:
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage, self.maxDurability = 63, False, 0, 63
		self.level = 0
	
	def isMatched(self, instrument):
		if not self.isBreakable:
			return False
		if isinstance(instrument, self.instrument):
			return True
		return False
	
	def getLoot(self):
		for i in range(len(self.loot)):
			if self.lootInfo[i][0]():
				count = random.randint(self.lootInfo[i][1], self.lootInfo[i][2])
				DatabaseStatic.static_world.locDroppedItems.append(self.loot[i](self.x, self.y, count))
	
	def ini(self):
		self.usableObject = False
		self.isThereCollisionEvent = False
	
	def doCollsiion(self):
		pass
	
	def useObject(self):
		pass
	
	def afterPlayerDiengUpdate(self):
		pass
	
	def relX(self, playerX):
		return self.x - playerX + 400
	
	def relY(self, playerY):
		return self.y - playerY + 300
	
	def update(self):
		pass
	
	def draw(self, surface):
		pass
	
	def destroy(self, power, level):
		if level < self.level:
			return
		
		self.durability -= power
		if self.durability <= 0:
			DatabaseStatic.static_world.locAdd(self.x, self.y, None)
			self.isBreaked = True
		else:
			fourPiece = self.maxDurability / 4
			for i in [4, 3, 2, 1]:
				if self.durability < fourPiece * i:
					self.destStage = 5 - i
	
	def outOfScreen(self):
		return self.x < 0 or self.x > 5120 or self.y < 0 or self.y > 5120
	
	def relOutOfScreen(self, playerX, playerY):
		return self.relX(playerX) + 32 < 0 or self.relX(playerX) > 800 or self.relY(playerY) + 32 < 0 or self.relY(playerY) > 600
	
	def drawXY(self, surface, playerX, playerY):
		pass

class GrowableGameObject(GameObject):
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.solid = False
		self.level = 1
		self.durability, self.isBreaked, self.destStage, self.maxDurability = 4, False, 0, 4
		self.production = None
	
	def initialize(self, mGroS, sTG):
		self.growStage, self.maxGrowStage, self.secondsToGrow = 0, mGroS, sTG + random.randint(2, 11)
		
		now = datetime.datetime.now()
		tempMinute = now.minute
		tempSecond = now.second
		tempHour = now.hour
		tempDay = now.day
		tempMonth = now.month
		tempYear = now.year
		del now
		
		self.stagesClick = []
		for i in range(self.maxGrowStage + 1):
			_sec = tempSecond + self.secondsToGrow * (i + 1)
			_min = tempMinute
			_hou = tempHour
			_day = tempDay
			_mon = tempMonth
			_yea = tempYear
			while _sec > 60:
				_sec -= 60
				_min += 1
				while _min > 60:
					_min -= 60
					_hou += 1
					while _hou > 24:
						_hou -= 24
						_day += 1
						while _day > 30:
							_day -= 30
							_mon += 1
							while _mon > 12:
								_mon -= 12
								_yea += 1
			self.stagesClick.append([_sec, _min, _hou, _day, _mon, _yea])
	
	def update(self):
		now = datetime.datetime.now()
		
		aStagesClick = list(self.stagesClick)
		aStagesClick.reverse()
		for i in range(len(aStagesClick)):
			yes = False
			if now.year > aStagesClick[i][5]:
				yes = True
			elif now.year == aStagesClick[i][5]:
				if now.month > aStagesClick[i][4]:
					yes = True
				elif now.month == aStagesClick[i][4]:
					if now.day > aStagesClick[i][3]:
						yes = True
					elif now.day == aStagesClick[i][3]:
						if now.hour > aStagesClick[i][2]:
							yes = True
						elif now.hour == aStagesClick[i][2]:
							if now.minute > aStagesClick[i][1]:
								yes = True
							elif now.minute == aStagesClick[i][1]:
								if now.second >= aStagesClick[i][0]:
									yes = True
			if yes:
				self.growStage = len(aStagesClick) - i
				if self.growStage >= self.maxGrowStage + 1:
					DatabaseStatic.static_world.locAdd(self.x, self.y, self.production(self.x, self.y))
					self.growStage = 0

class GUIGameObject(GameObject):
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.sprite = None
		self.durability, self.isBreaked, self.destStage, self.maxDurability = 63, False, 0, 63
		self.level = 0
		
		self.guiInitialize()
	
	def destroy(self, power, level):
		if level < self.level:
			return
		
		self.durability -= power
		if self.durability <= 0:
			DatabaseStatic.static_world.locAdd(self.x, self.y, None)
			self.isBreaked = True
			self.guiUninitialize()
		else:
			fourPiece = self.maxDurability / 4
			for i in [4, 3, 2, 1]:
				if self.durability < fourPiece * i:
					self.destStage = 5 - i
	
	def enter(self):
		pass
	
	def developCraft(self):
		pass
	
	def guiInitialize(self):
		pass
	
	def guiStart(self):
		pass
	
	def guiUpdate(self):
		pass
	
	def guiDraw(self, surface, mouseX, mouseY):
		pass
	
	def guiClose(self):
		pass
	
	def guiUninitialize(self):
		pass

class DroppedItem(GameObject):
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.sprite = None
		self.item = None
	
	def update(self):
		pass
	
	def draw(self, surface):
		pass
	
	def outOfScreen(self):
		return self.x < 0 or self.x > 5120 or self.y < 0 or self.y > 5120
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(self.sprite.getSprite(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class TableItem(Item):
	
	systemName = "table"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Table")
		self.titles = [mp.localyze("The table")]
		
		self.ini()
		
		self.putObject = TableObject
	
	def getSprite(self):
		return tableSprite
	
	def getSingleComponent(self):
		return TableItem()
	
	def getInDropped(self, x, y):
		return DroppedTable(x, y, self.count)

class BirchTableItem(Item):
	
	systemName = "birchtable"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Birch Table")
		self.titles = [mp.localyze("The birch table")]
		
		self.ini()
		
		self.putObject = BirchTableObject
	
	def getSprite(self):
		return birchtableSprite
	
	def getSingleComponent(self):
		return BirchTableItem()
	
	def getInDropped(self, x, y):
		return DroppedBirchTable(x, y, self.count)

class CactusTableItem(Item):
	
	systemName = "cactustable"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Cactus Table")
		self.titles = [mp.localyze("The cactus table")]
		
		self.ini()
		
		self.putObject = CactusTableObject
	
	def getSprite(self):
		return cactustableSprite
	
	def getSingleComponent(self):
		return CactusTableItem()
	
	def getInDropped(self, x, y):
		return DroppedCactusTable(x, y, self.count)

class ClearCactusTableItem(Item):
	
	systemName = "cactitablclean"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Peeled Cactus Table")
		self.titles = [mp.localyze("The table is made of peeled cactus")]
		
		self.ini()
		
		self.putObject = ClearCactusTableObject
	
	def getSprite(self):
		return clearcactustableSprite
	
	def getSingleComponent(self):
		return ClearCactusTableItem()
	
	def getInDropped(self, x, y):
		return DroppedClearCactusTable(x, y, self.count)

class ChairItem(Item):
	
	systemName = "chair"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("The Chair")
		self.titles = []
		
		self.ini()
		
		self.putObject = ChairObject
	
	def getSprite(self):
		return leftchairSprite
	
	def getSingleComponent(self):
		return ChairItem()
	
	def getInDropped(self, x, y):
		return DroppedChair(x, y, self.count)

class BirchChairItem(Item):
	
	systemName = "birchchair"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("The Birch Chair")
		self.titles = []
		
		self.ini()
		
		self.putObject = BirchChair
	
	def getSprite(self):
		return leftbirchchair
	
	def getSingleComponent(self):
		return BirchChairItem()
	
	def getInDropped(self, x, y):
		return DroppedBirchChair(x, y, self.count)

class CactusChairItem(Item):
	
	systemName = "cactichair"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("The Cactus Chair")
		self.titles = []
		
		self.ini()
		
		self.putObject = CactusChair
	
	def getSprite(self):
		return leftcactuschair
	
	def getSingleComponent(self):
		return CactusChairItem()
	
	def getInDropped(self, x, y):
		return DroppedCactusChair(x, y, self.count)

class ClearCactusChairItem(Item):
	
	systemName = "clearcactichair"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("The Chair made of peeled cactus")
		self.titles = []
		
		self.ini()
		
		self.putObject = ClearCactusChair
	
	def getSprite(self):
		return leftclearcactuschair
	
	def getSingleComponent(self):
		return ClearCactusChairItem()
	
	def getInDropped(self, x, y):
		return DroppedClearCactusChair(x, y, self.count)

class WoodLinoleumItem(Item):
	
	systemName = "woodlinoleum"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Wood Linoleum")
		self.titles = []
		
		self.ini()
		
		self.putObject = WoodLinoleumObject
	
	def getSprite(self):
		return woodlinoleumSprite
	
	def getSingleComponent(self):
		return WoodLinoleumItem()
	
	def getInDropped(self, x, y):
		return DroppedWoodLinoleum(x, y, self.count)

class BirchLinoleumItem(Item):
	
	systemName = "birchlinoleum"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Birch Linoleum")
		self.titles = []
		
		self.ini()
		
		self.putObject = BirchLinoleumObject
	
	def getSprite(self):
		return birchlinoleumSprite
	
	def getSingleComponent(self):
		return BirchLinoleumItem()
	
	def getInDropped(self, x, y):
		return DroppedBirchLinoleum(x, y, self.count)

class CactusLinoleumItem(Item):
	
	systemName = "cactuslinoleum"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Cactus Linoleum")
		self.titles = []
		
		self.ini()
		
		self.putObject = CactusLinoleumObject
	
	def getSprite(self):
		return cactuslinoleumSprite
	
	def getSingleComponent(self):
		return CactusLinoleumItem()
	
	def getInDropped(self, x, y):
		return DroppedCactusLinoleum(x, y, self.count)

class ClearCactusLinoleumItem(Item):
	
	systemName = "cleancactilino"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Linoleum made of peeled cactus")
		self.titles = []
		
		self.ini()
		
		self.putObject = ClearCactusLinoleumObject
	
	def getSprite(self):
		return clearcactuslinoleumSprite
	
	def getSingleComponent(self):
		return ClearCactusLinoleumItem()
	
	def getInDropped(self, x, y):
		return DroppedClearCactusLinoleum(x, y, self.count)

class WoodDoorItem(Item):
	
	systemName = "wooddoor"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Wooden Door")
		self.titles = []
		
		self.ini()
		
		self.putObject = WoodDoorObject
	
	def getSprite(self):
		return wooddoorcloseSprite
	
	def getSingleComponent(self):
		return WoodDoorItem()
	
	def getInDropped(self, x, y):
		return DroppedWoodDoor(x, y, self.count)

class BirchDoorItem(Item):
	
	systemName = "birchdoor"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Birch Door")
		self.titles = []
		
		self.ini()
		
		self.putObject = BirchDoorObject
	
	def getSprite(self):
		return birchdoorcloseSprite
	
	def getSingleComponent(self):
		return BirchDoorItem()
	
	def getInDropped(self, x, y):
		return DroppedBirchDoor(x, y, self.count)

class CactusDoorItem(Item):
	
	systemName = "cactidoor"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Cactus Door")
		self.titles = []
		
		self.ini()
		
		self.putObject = CactusDoorObject
	
	def getSprite(self):
		return cactusdoorcloseSprite
	
	def getSingleComponent(self):
		return CactusDoorItem()
	
	def getInDropped(self, x, y):
		return DroppedCactusDoor(x, y, self.count)

class ClearCactusDoorItem(Item):
	
	systemName = "cleancactidoor"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("A Door made of peeled cactus")
		self.titles = []
		
		self.ini()
		
		self.putObject = ClearCactusDoorObject
	
	def getSprite(self):
		return clearcactusdoorcloseSprite
	
	def getSingleComponent(self):
		return ClearCactusDoorItem()
	
	def getInDropped(self, x, y):
		return DroppedClearCactusDoor(x, y, self.count)

class ClearCactusItem(Item):
	
	systemName = "clearcacti"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Peeled Cactus")
		self.titles = [mp.localyze("Just the peeled cactus..")]
		
		self.ini()
	
	def getSprite(self):
		return clearcactusSprite
	
	def getSingleComponent(self):
		return ClearCactusItem()
	
	def getInDropped(self, x, y):
		return DroppedClearCactus(x, y, self.count)

class BirchSaplingItem(Item):
	
	systemName = "birchsapling"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Birch Sapling")
		self.titles = [mp.localyze("This is birch acorn!")]
		
		self.ini()
		
		self.putObject = BirchSaplingObject
	
	def getSprite(self):
		return iBirchSaplingItemSprite
	
	def getSingleComponent(self):
		return BirchSaplingItem()
	
	def getInDropped(self, x, y):
		return DroppedBirchSapling(x, y, self.count)

class BirchWoodItem(Item):
	
	systemName = "birchwood"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Birch Wood")
		self.titles = [mp.localyze("Is it birch wood? That can not be!")]
		
		self.ini()
		
		self.putObject = BirchWoodPlankObject
	
	def getSprite(self):
		return iBirchWoodItemSprite
	
	def getSingleComponent(self):
		return BirchWoodItem()
	
	def getInDropped(self, x, y):
		return DroppedBirchWood(x, y, self.count)

class AcornItem(Item):
	
	systemName = "acorn"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Acorn")
		self.titles = [mp.localyze("You can plant it")]
		
		self.ini()
		
		self.putObject = WoodSaplingObject
	
	def getSprite(self):
		return iAcornSprite
	
	def getSingleComponent(self):
		return AcornItem()
	
	def getInDropped(self, x, y):
		return DroppedAcorn(x, y, self.count)

class AppleItem(Item):
	
	systemName = "apple"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Apple")
		self.titles = [mp.localyze("It can restore 10 HP"), mp.localyze("1080 Apples...")]
		
		self.ini()
		
		self.usableItem = True
	
	def useItem(self):
		if DatabaseStatic.static_player.effectManager.getEffectIndex(HealingDelayEffect) == None:
			DatabaseStatic.static_player.effectManager.addEffect(HealingDelayEffect(25))
			DatabaseStatic.static_player.effectManager.addEffect(HpRestoreEffect(7))
			DatabaseStatic.static_player.inventory.accessPanel.minus()
	
	def getSprite(self):
		return iAppleSprite
	
	def getSingleComponent(self):
		return AppleItem()
	
	def getInDropped(self, x, y):
		return DroppedApple(x, y, self.count)

class CactusItem(Item):
	
	systemName = "cactus"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Cactus")
		self.titles = [mp.localyze("Is it cactus planks?")]
		
		self.ini()
	
	def getSprite(self):
		return iDroppedcactusSprite
	
	def getSingleComponent(self):
		return CactusItem()
	
	def getInDropped(self, x, y):
		return DroppedCactus(x, y, self.count)

class RedFlowerItem(Item):
	
	systemName = "rf"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Red Flower")
		self.titles = [mp.localyze("It can't flip its color")]
		
		self.ini()
		
		self.putObject = RedFlowerObject
	
	def getSprite(self):
		return iAFlowerSprites[0]
	
	def getSingleComponent(self):
		return RedFlowerItem()
	
	def getInDropped(self, x, y):
		return DroppedRedFlower(x, y, self.count)

class OrangeFlowerItem(Item):
	
	systemName = "of"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Orange Flower")
		self.titles = [mp.localyze("It can't flip its color")]
		
		self.ini()
		
		self.putObject = OrangeFlowerObject
	
	def getSprite(self):
		return iAFlowerSprites[1]
	
	def getSingleComponent(self):
		return OrangeFlowerItem()
	
	def getInDropped(self, x, y):
		return DroppedOrangeFlower(x, y, self.count)

class BlueFlowerItem(Item):
	
	systemName = "bf"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Blue Flower")
		self.titles = [mp.localyze("It can't flip its color")]
		
		self.ini()
		
		self.putObject = BlueFlowerObject
	
	def getSprite(self):
		return iAFlowerSprites[2]
	
	def getSingleComponent(self):
		return BlueFlowerItem()
	
	def getInDropped(self, x, y):
		return DroppedBlueFlower(x, y, self.count)

class PinkFlowerItem(Item):
	
	systemName = "pf"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Pink Flower")
		self.titles = [mp.localyze("It can't flip its color")]
		
		self.ini()
		
		self.putObject = PinkFlowerObject
	
	def getSprite(self):
		return iAFlowerSprites[3]
	
	def getSingleComponent(self):
		return PinkFlowerItem()
	
	def getInDropped(self, x, y):
		return DroppedPinkFlower(x, y, self.count)

class MarbleItem(Item):
	
	systemName = "marble"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Marble")
		self.titles = [mp.localyze("Its not stone")]
		
		self.ini()
		
		self.putObject = MarbleObject
	
	def getSprite(self):
		return iDroppedmarbleSprite
	
	def getSingleComponent(self):
		return MarbleItem()
	
	def getInDropped(self, x, y):
		return DroppedMarble(x, y, self.count)

class HoneyItem(Item):
	
	systemName = "honey2801"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Honey")
		self.titles = [mp.localyze("This honey is not made by bees.")]
		
		self.ini()
		
		self.usableItem = True
	
	def useItem(self):
		if DatabaseStatic.static_player.effectManager.getEffectIndex(HealingDelayEffect) == None:
			DatabaseStatic.static_player.effectManager.addEffect(HealingDelayEffect(25))
			DatabaseStatic.static_player.effectManager.addEffect(HpRestoreEffect2(3))
			DatabaseStatic.static_player.inventory.accessPanel.minus()
	
	def getSprite(self):
		return iHoney
	
	def getSingleComponent(self):
		return HoneyItem()
	
	def getInDropped(self, x, y):
		return DroppedHoney(x, y, self.count)

class MysteryFlowerItem(Item):
	
	systemName = "mystflower"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Mysterious Flower")
		self.titles = [mp.localyze("One of a kind"), mp.localyze("You will regret having stolen it")]
		
		self.ini()
		
		self.putObject = MysteryFlowerObject
	
	def getSprite(self):
		return iDroppedmysteryflowerSprite
	
	def getSingleComponent(self):
		return MysteryFlowerItem()
	
	def getInDropped(self, x, y):
		return DroppedMysteryFlower(x, y, self.count)

class MysteryStoneItem(Item):
	
	systemName = "myststone"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Mystery Marble")
		self.titles = [mp.localyze("Someone drew this drawing")]
		
		self.ini()
		
		self.putObject = MysteryStoneObject
	
	def getSprite(self):
		return iDroppedmysterystoneSprite
	
	def getSingleComponent(self):
		return MysteryStoneItem()
	
	def getInDropped(self, x, y):
		return DroppedMysteryStone(x, y, self.count)

class SandItem(Item):
	
	systemName = "sand"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Sand")
		self.titles = [mp.localyze("The sand is not frayed")]
		
		self.ini()
		
		self.putObject = SandObject
	
	def getSprite(self):
		return iDroppedsandSprite
	
	def getSingleComponent(self):
		return SandItem()
	
	def getInDropped(self, x, y):
		return DroppedSand(x, y, self.count)

class WoodItem(Item):
	
	systemName = "wood"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Oak Wood")
		self.titles = [mp.localyze("Why birch wood is not birch?")]
		
		self.ini()
		
		self.putObject = WoodPlankObject
	
	def getSprite(self):
		return iDroppedwoodSprite
	
	def getSingleComponent(self):
		return WoodItem()
	
	def getInDropped(self, x, y):
		return DroppedWood(x, y, self.count)

class CoffinItem(Item):
	
	systemName = "coffin"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Coffin")
		self.titles = [mp.localyze("Who is buried in the coffin?")]
		
		self.ini()
		
		self.putObject = CoffinObject
	
	def getSprite(self):
		return coffinSprite
	
	def getSingleComponent(self):
		return CoffinItem()
	
	def getInDropped(self, x, y):
		return DroppedCoffin(x, y, self.count)

class WorkbenchItem(Item):
	
	systemName = "workbench"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Workbench")
		self.titles = [mp.localyze("That is crafting station")]
		
		self.ini()
		
		self.putObject = WorkbenchObject
	
	def getSprite(self):
		return iDroppedworkbenchSprite
	
	def getSingleComponent(self):
		return WorkbenchItem()
	
	def getInDropped(self, x, y):
		return DroppedWorkbench(x, y, self.count)

class BirchWorkbenchItem(Item):
	
	systemName = "birchworkbench"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Workbench made of birch wood")
		self.titles = [mp.localyze("This is crafting station")]
		
		self.ini()
		
		self.putObject = BirchWorkbenchObject
	
	def getSprite(self):
		return birchworkbenchSprite
	
	def getSingleComponent(self):
		return BirchWorkbenchItem()
	
	def getInDropped(self, x, y):
		return DroppedBirchWorkbench(x, y, self.count)

class ChestItem(Item):
	
	systemName = "chestnor"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Wooden Chest")
		self.titles = [mp.localyze("This is storage for your items")]
		
		self.ini()
		
		self.putObject = ChestObject
	
	def getSprite(self):
		return woodchestSprite
	
	def getSingleComponent(self):
		return ChestItem()
	
	def getInDropped(self, x, y):
		return DroppedChest(x, y, self.count)

class BirchChestItem(Item):
	
	systemName = "chestnorbirch"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Birch Chest")
		self.titles = [mp.localyze("This is storage for your items")]
		
		self.ini()
		
		self.putObject = BirchChestObject
	
	def getSprite(self):
		return birchchestSprite
	
	def getSingleComponent(self):
		return BirchChestItem()
	
	def getInDropped(self, x, y):
		return DroppedBirchChest(x, y, self.count)

class CactusChestItem(Item):
	
	systemName = "chestnorcacti"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Cactus Chest")
		self.titles = [mp.localyze("This is storage for your items")]
		
		self.ini()
		
		self.putObject = CactusChestObject
	
	def getSprite(self):
		return cactuschestSprite
	
	def getSingleComponent(self):
		return CactusChestItem()
	
	def getInDropped(self, x, y):
		return DroppedCactusChest(x, y, self.count)

class ClearCactusChestItem(Item):
	
	systemName = "chestnorcacticlean"
	
	def __init__(self, count = 1):
		self.count = count
		self.itemName = mp.localyze("Chest made of peeled cactus")
		self.titles = [mp.localyze("This is storage for your items")]
		
		self.ini()
		
		self.putObject = ClearCactusChestObject
	
	def getSprite(self):
		return clearcactuschestSprite
	
	def getSingleComponent(self):
		return ClearCactusChestItem()
	
	def getInDropped(self, x, y):
		return DroppedClearCactusChest(x, y, self.count)

class WeaponItem(Item):
	
	def __init__(self, count = 1):
		self.systemName = ""
		self.count = count
		self.itemName = ""
		self.titles = []
		self.damage = 0
		self.level = 0

class SwordItem(WeaponItem):
	
	def __init__(self, count = 1):
		self.systemName = ""
		self.count = count
		self.itemName = ""
		self.titles = []
		self.damage = 0
		self.radius = 0
		self.level = 0

class WoodenSword(SwordItem):
	
	systemName = "woodsword"
	damage = 10
	radius = 64
	speed = 127
	
	def __init__(self):
		self.count = 1
		self.itemName = mp.localyze("Wooden sword")
		self.titles = [mp.localyze("It can kill entities"), mp.localyze("And it feels a big grudge")]
		
		self.ini()
	
	def getSprite(self):
		return iWoodenswordSprite
	
	def getSingleComponent(self):
		return self
	
	def getInDropped(self, x, y):
		return DroppedWoodenSword(x, y)

class AxeItem(Item):
	
	def __init__(self, count = 1):
		self.systemName = ""
		self.count = count
		self.itemName = ""
		self.titles = []
		self.power = 0
		self.level = 0

class WoodenAxe(AxeItem):
	
	systemName = "woodax"
	power = 1
	radius = 64
	level = 1
	
	def __init__(self):
		self.count = 1
		self.itemName = mp.localyze("Wooden axe")
		self.titles = [mp.localyze("It can cut a trees"), mp.localyze("And it feels a big grudge")]
		
		self.ini()
	
	def getSprite(self):
		return iWoodenaxeSprite
	
	def getSingleComponent(self):
		return self
	
	def getInDropped(self, x, y):
		return DroppedWoodenAxe(x, y)

class PickaxeItem(Item):
	
	def __init__(self, count = 1):
		self.systemName = ""
		self.count = count
		self.itemName = ""
		self.titles = []
		self.power = 0
		self.level = 0

class WoodenPickaxe(PickaxeItem):
	
	systemName = "woodpickax"
	power = 1
	radius = 64
	level = 1
	
	def __init__(self):
		self.count = 1
		self.itemName = mp.localyze("Wooden pickaxe")
		self.titles = [mp.localyze("It can break a stones"), mp.localyze("And it feels a big grudge")]
		
		self.ini()
	
	def getSprite(self):
		return iWoodenpickaxeSprite
	
	def getSingleComponent(self):
		return self
	
	def getInDropped(self, x, y):
		return DroppedWoodenPickaxe(x, y)

class DroppedTable(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = TableItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(tableSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedBirchTable(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = BirchTableItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(birchtableSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedCactusTable(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = CactusTableItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(cactustableSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedClearCactusTable(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = ClearCactusTableItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(clearcactustableSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedChair(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = ChairItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(leftchairSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedBirchChair(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = BirchChairItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(leftbirchchair, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedCactusChair(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = CactusChairItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(leftcactuschair, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedClearCactusChair(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = ClearCactusChairItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(leftclearcactuschair, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedWoodLinoleum(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = WoodLinoleumItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(woodlinoleumSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedBirchLinoleum(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = BirchLinoleumItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(birchlinoleumSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedCactusLinoleum(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = CactusLinoleumItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(cactuslinoleumSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedWoodDoor(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = WoodDoorItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(wooddoorcloseSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedBirchDoor(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = BirchDoorItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(birchdoorcloseSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedCactusDoor(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = CactusDoorItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(cactusdoorcloseSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedClearCactusDoor(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = ClearCactusDoorItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(clearcactusdoorcloseSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedClearCactusLinoleum(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = ClearCactusLinoleumItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(clearcactuslinoleumSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedClearCactus(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = ClearCactusItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(clearcactusSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedBirchSapling(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = BirchSaplingItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dDroppedBirchSaplingSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedBirchWood(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = BirchWoodItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dDroppedBirchWoodSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedAcorn(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = AcornItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dAcornSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedApple(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = AppleItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dAppleSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedCactus(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = CactusItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dDroppedcactusSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedRedFlower(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = RedFlowerItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(diAFlowerSprites[0], [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedOrangeFlower(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = OrangeFlowerItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(diAFlowerSprites[1], [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedBlueFlower(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = BlueFlowerItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(diAFlowerSprites[2], [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedPinkFlower(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = PinkFlowerItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(diAFlowerSprites[3], [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedMarble(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = MarbleItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dDroppedmarbleSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedHoney(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = HoneyItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(iHoney, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedMysteryFlower(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = MysteryFlowerItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dDroppedmysteryflowerSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedMysteryStone(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = MysteryStoneItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dDroppedmysterystoneSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedSand(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = SandItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dDroppedsandSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedWood(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = WoodItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dDroppedwoodSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedCoffin(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = CoffinItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(coffinSprite, [self.x - playerX + 400, self.y - playerY + 300])

class DroppedWorkbench(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = WorkbenchItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dDroppedworkbenchSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedBirchWorkbench(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = BirchWorkbenchItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(birchworkbenchSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedChest(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = ChestItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(woodchestSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedBirchChest(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = BirchChestItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(birchchestSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedCactusChest(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = CactusChestItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(cactuschestSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedClearCactusChest(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y, count = 1):
		self.x = x
		self.y = y
		self.item = ClearCactusChestItem(count)
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(clearcactuschestSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedWoodenSword(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.item = WoodenSword()
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dWoodenswordSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedWoodenAxe(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.item = WoodenAxe()
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dWoodenaxeSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class DroppedWoodenPickaxe(DroppedItem):
	
	solid = False
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.item = WoodenPickaxe()
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(dWoodenpickaxeSprite, [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class CactusObject(GameObject):
	
	solid = False
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedCactus,)
	lootInfo = ((lambda: True, 4, 8),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 32, False, 0
		self.ini()
	
	def destroy(self, power, level):
		if level < self.level:
			return
		
		self.durability -= power
		if self.durability <= 0:
			self.isBreaked = True
		else:
			fourPiece = self.maxDurability / 4
			for i in [4, 3, 2, 1]:
				if self.durability < fourPiece * i:
					self.destStage = 5 - i
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(cactusSprite, [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class CactusSaplingObject(GrowableGameObject):
	
	solid = False
	level = 1
	production = CactusObject
	maxDurability = 4
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedCactus,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.solid = False
		self.level = 1
		self.durability, self.isBreaked, self.destStage = 4, False, 0
		
		self.ini()
		
		self.initialize(3, 70)
	
	def destroy(self, power, level):
		if level < self.level:
			return
		
		self.durability -= power
		if self.durability <= 0:
			self.isBreaked = True
		else:
			fourPiece = self.maxDurability / 4
			for i in [4, 3, 2, 1]:
				if self.durability < fourPiece * i:
					self.destStage = 5 - i
	
	def update(self):
		now = datetime.datetime.now()
		
		aStagesClick = list(self.stagesClick)
		aStagesClick.reverse()
		for i in range(len(aStagesClick)):
			yes = False
			if now.year > aStagesClick[i][5]:
				yes = True
			elif now.year == aStagesClick[i][5]:
				if now.month > aStagesClick[i][4]:
					yes = True
				elif now.month == aStagesClick[i][4]:
					if now.day > aStagesClick[i][3]:
						yes = True
					elif now.day == aStagesClick[i][3]:
						if now.hour > aStagesClick[i][2]:
							yes = True
						elif now.hour == aStagesClick[i][2]:
							if now.minute > aStagesClick[i][1]:
								yes = True
							elif now.minute == aStagesClick[i][1]:
								if now.second >= aStagesClick[i][0]:
									yes = True
			if yes:
				self.growStage = len(aStagesClick) - i
				if self.growStage >= self.maxGrowStage + 1:
					DatabaseStatic.static_world.locGet(self.x, self.y).setOn(self.production(self.x, self.y))
					self.growStage = 0
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(cactusGrows[self.growStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class RedFlowerObject(GameObject):
	
	level = 1
	solid = False
	maxDurability = 4
	
	isBreakable = True
	instrument = PickaxeItem
	loot = (DroppedRedFlower,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 4, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(flowersSprites[0].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class OrangeFlowerObject(GameObject):
	
	solid = False
	maxDurability = 4
	level = 1
	
	isBreakable = True
	instrument = PickaxeItem
	loot = (DroppedOrangeFlower,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 4, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(flowersSprites[1].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class BlueFlowerObject(GameObject):
	
	level = 1
	solid = False
	maxDurability = 4
	
	isBreakable = True
	instrument = PickaxeItem
	loot = (DroppedBlueFlower,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 4, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(flowersSprites[2].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class PinkFlowerObject(GameObject):
	
	level = 1
	solid = False
	maxDurability = 4
	
	isBreakable = True
	instrument = PickaxeItem
	loot = (DroppedPinkFlower,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 4, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(flowersSprites[3].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class MarbleObject(GameObject):
	
	level = 2
	maxDurability = 128
	solid = True
	
	isBreakable = True
	instrument = PickaxeItem
	loot = (DroppedMarble,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 128, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(marbleSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class MysteryFlowerObject(GameObject):
	
	solid = False
	level = 1
	maxDurability = 8
	
	isBreakable = True
	instrument = PickaxeItem
	loot = (DroppedMysteryFlower,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 8, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(mysteryFlowerSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class MysteryStoneObject(GameObject):
	
	solid = True
	maxDurability = 256
	level = 3
	
	isBreakable = True
	instrument = PickaxeItem
	loot = (DroppedMysteryStone,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 256, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(mysteryStoneSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class SandObject(GameObject):
	
	solid = False
	maxDurability = 12
	level = 1
	
	isBreakable = True
	instrument = PickaxeItem
	loot = (DroppedSand,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 12, False, 0
		self.on = None
		
		self.ini()
		
		self.isThereCollisionEvent = True
	
	def doCollsiion(self):
		player = DatabaseStatic.static_player
		
		if self.on != None and type(self.on) == CactusObject:
			if DatabaseStatic.static_player.effectManager.getEffectIndex(CutEffect2) == None:
				DatabaseStatic.static_player.effectManager.addEffect(CutEffect2(2))
	
	def setOn(self, on2):
		if on2 != None:
			self.on = on2
			self.solid = on2.solid
		else:
			self.on = None
			self.solid = False
	
	def update(self):
		if self.on != None:
			self.on.update()
		elif round(random.random(), 7) == 0.1:
			self.on = CactusSaplingObject(self.x, self.y)
	
	def drawXY(self, surface, playerX, playerY):
		pyg.draw.rect(surface, [255, 142, 0], [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		
		if self.on != None:
			self.on.drawXY(surface, playerX, playerY)

class TreeObject(GameObject):
	
	solid = True
	level = 1
	maxDurability = 64
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedWood, DroppedAcorn, DroppedApple)
	lootInfo = ((lambda: True, 2, 4), (lambda: random.choice([False, True, True, True, True]), 1, 2), (lambda: random.choice([False]*9+[True]), 1, 1))
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 64, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(treesSprites[0].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class BirchObject(GameObject):
	
	solid = True
	level = 1
	maxDurability = 64
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedBirchWood, DroppedBirchSapling)
	lootInfo = ((lambda: True, 2, 4), (lambda: random.choice([False, True, True, True, True]), 1, 2))
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 64, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(treesSprites[1].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class HoneyBirchObject(GameObject):
	
	solid = True
	level = 1
	maxDurability = 64
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedBirchWood, DroppedBirchSapling)
	lootInfo = ((lambda: True, 2, 4), (lambda: random.choice([False, True, True, True, True]), 1, 2))
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 64, False, 0
		
		#0-With Honey, 1-Without Honey
		self.beehiveState = 0
		
		self.ini()
		self.initialize(1, 50)
		
		self.usableObject = True
	
	def getLoot(self):
		for i in range(len(self.loot)):
			if self.lootInfo[i][0]():
				count = random.randint(self.lootInfo[i][1], self.lootInfo[i][2])
				DatabaseStatic.static_world.locDroppedItems.append(self.loot[i](self.x, self.y, count))
		if self.beehiveState == 0:
			DatabaseStatic.static_world.locDroppedItems.append(DroppedHoney(self.x, self.y, 1))
	
	def useObject(self):
		if self.beehiveState == 0:
			DatabaseStatic.static_world.locDroppedItems.append(DroppedHoney(self.x, self.y, 1))
			self.beehiveState = 1
	
	def initialize(self, mGroS, sTG):
		self.growStage, self.maxGrowStage, self.secondsToGrow = 0, mGroS, sTG + random.randint(2, 11)
		
		now = datetime.datetime.now()
		tempMinute = now.minute
		tempSecond = now.second
		tempHour = now.hour
		tempDay = now.day
		tempMonth = now.month
		tempYear = now.year
		del now
		
		self.stagesClick = []
		for i in range(self.maxGrowStage + 1):
			_sec = tempSecond + self.secondsToGrow * (i + 1)
			_min = tempMinute
			_hou = tempHour
			_day = tempDay
			_mon = tempMonth
			_yea = tempYear
			while _sec > 60:
				_sec -= 60
				_min += 1
				while _min > 60:
					_min -= 60
					_hou += 1
					while _hou > 24:
						_hou -= 24
						_day += 1
						while _day > 30:
							_day -= 30
							_mon += 1
							while _mon > 12:
								_mon -= 12
								_yea += 1
			self.stagesClick.append([_sec, _min, _hou, _day, _mon, _yea])
	
	def update(self):
		if self.beehiveState == 0:
			return
		
		now = datetime.datetime.now()
		
		aStagesClick = list(self.stagesClick)
		aStagesClick.reverse()
		for i in range(len(aStagesClick)):
			yes = False
			if now.year > aStagesClick[i][5]:
				yes = True
			elif now.year == aStagesClick[i][5]:
				if now.month > aStagesClick[i][4]:
					yes = True
				elif now.month == aStagesClick[i][4]:
					if now.day > aStagesClick[i][3]:
						yes = True
					elif now.day == aStagesClick[i][3]:
						if now.hour > aStagesClick[i][2]:
							yes = True
						elif now.hour == aStagesClick[i][2]:
							if now.minute > aStagesClick[i][1]:
								yes = True
							elif now.minute == aStagesClick[i][1]:
								if now.second >= aStagesClick[i][0]:
									yes = True
			if yes:
				self.growStage = len(aStagesClick) - i
				if self.growStage >= self.maxGrowStage + 1:
					self.beehiveState = 0
					self.growStage = 0
					self.initialize(1, 50)
	
	def drawXY(self, surface, playerX, playerY):
		if self.beehiveState == 0:
			surface.blit(honeyAnimation.getSprite().convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		else:
			surface.blit(beehivebirchSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class WaterObject(GameObject):
	
	solid = False
	level = 1
	
	isBreakable = False
	instrument = AxeItem
	loot = tuple([])
	lootInfo = tuple([])
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
		self.ini()
		
		self.isThereCollisionEvent = True
	
	def doCollsiion(self):
		player = DatabaseStatic.static_player
		
		player.isShip = True
		if player.sprayCooldown == 0:
			if player.particlesLevel > 0:
				dir = [0, 0]
				dir[0] = 1 if player.left else (-1 if player.right else 0)
				dir[1] = 1 if player.up else (-1 if player.down else 0)
				if dir[0] != 0 or dir[1] != 0:
					player.waterSprays.append(WaterSpray(player.x, player.y, tuple(dir), 180))
				player.sprayCooldown = 90
		else:
			player.sprayCooldown -= 0.25
	
	def drawXY(self, surface, playerX, playerY):
		pyg.draw.rect(surface, [0, 0, 255], [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class CoffinObject(GameObject):
	
	solid = True
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedCoffin,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 32, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(coffinSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class TableObject(GameObject):
	
	solid = True
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedTable,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 32, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(tableSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class BirchTableObject(GameObject):
	
	solid = True
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedBirchTable,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 32, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(birchtableSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class CactusTableObject(GameObject):
	
	solid = True
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedCactusTable,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 32, False, 0
		
		self.ini()
		
		self.isThereCollisionEvent = True
	
	def doCollsiion(self):
		if DatabaseStatic.static_player.effectManager.getEffectIndex(CutEffect) == None:
			DatabaseStatic.static_player.effectManager.addEffect(CutEffect(3))
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(cactustableSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class ClearCactusTableObject(GameObject):
	
	solid = True
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedClearCactusTable,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 32, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(clearcactustableSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class ChairObject(GameObject):
	
	solid = False
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedChair,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 32, False, 0
		
		self.ini()
		
		self.usableObject = True
		self.isThereCollisionEvent = True
		
		self.dir = 0
		self.oldMovespeed = 0
		self.sited = False
	
	def seedown(self):
		self.oldMovespeed = int(DatabaseStatic.static_player.moveSpeed)
		DatabaseStatic.static_player.moveSpeed = 0
		
		DatabaseStatic.static_player.x = self.x + (-5 if self.dir == 0 else 5)
		DatabaseStatic.static_player.y = self.y - 7
		
		self.isBreakable = False
		self.sited = True
	
	def seeup(self):
		DatabaseStatic.static_player.moveSpeed = int(self.oldMovespeed)
		self.oldMovespeed = 0
		
		self.sited = False
		self.isBreakable = True
	
	def afterPlayerDiengUpdate(self):
		self.seeup()
	
	def doCollsiion(self):
		if not self.sited:
			self.seedown()
	
	def update(self):
		if self.sited:
			if pyg.key.get_pressed()[pyg.K_w]:
				self.seeup()
				if self.y - 32 < 32:
					DatabaseStatic.static_player.y += 64
				else:
					DatabaseStatic.static_player.y -= 32
			else:
				DatabaseStatic.static_player.sprite = self.getPlayersSprite()
	
	def useObject(self):
		if not self.sited:
			self.dir = 0 if self.dir == 1 else 1
	
	def getSprite(self):
		return leftchairSprite if self.dir == 0 else rightchairSprite
	
	def getPlayersSprite(self):
		return playerSits[self.dir]
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(self.getSprite(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class BirchChair(ChairObject):
	
	solid = False
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedBirchChair,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def getSprite(self):
		return leftbirchchair if self.dir == 0 else rightbirchchair

class CactusChair(ChairObject):
	
	solid = False
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedCactusChair,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def update(self):
		if self.sited:
			if pyg.key.get_pressed()[pyg.K_w]:
				self.seeup()
				if self.y - 32 < 32:
					DatabaseStatic.static_player.y += 64
				else:
					DatabaseStatic.static_player.y -= 32
			else:
				DatabaseStatic.static_player.sprite = self.getPlayersSprite()
				
				if DatabaseStatic.static_player.effectManager.getEffectIndex(CutEffect) == None:
					DatabaseStatic.static_player.effectManager.addEffect(CutEffect(3))
	
	def getSprite(self):
		return leftcactuschair if self.dir == 0 else rightcactuschair

class ClearCactusChair(ChairObject):
	
	solid = False
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedClearCactusChair,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def getSprite(self):
		return leftclearcactuschair if self.dir == 0 else rightclearcactuschair

class WoodLinoleumObject(GameObject):
	
	solid = False
	level = 1
	maxDurability = 12
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedWoodLinoleum,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 12, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(woodlinoleumSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class BirchLinoleumObject(GameObject):
	
	solid = False
	level = 1
	maxDurability = 12
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedBirchLinoleum,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 12, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(birchlinoleumSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class CactusLinoleumObject(GameObject):
	
	solid = False
	level = 1
	maxDurability = 12
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedCactusLinoleum,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 12, False, 0
		
		self.ini()
		
		self.isThereCollisionEvent = True
	
	def doCollsiion(self):
		if DatabaseStatic.static_player.effectManager.getEffectIndex(CutEffect) == None:
			DatabaseStatic.static_player.effectManager.addEffect(CutEffect(3))
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(cactuslinoleumSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class ClearCactusLinoleumObject(GameObject):
	
	solid = False
	level = 1
	maxDurability = 12
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedClearCactusLinoleum,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 12, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(clearcactuslinoleumSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class WoodDoorObject(GameObject):
	
	level = 1
	maxDurability = 48
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedWoodDoor,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 48, False, 0
		
		self.ini()
		
		self.usableObject = True
		self.isThereCollisionEvent = True
		self.solid = False
		
		self.isClosed = True
	
	def collEvent2(self):
		pass
	
	def doCollsiion(self):
		if self.isClosed:
			self.solid = DatabaseStatic.static_player.up or DatabaseStatic.static_player.down
		else:
			self.solid = DatabaseStatic.static_player.left or DatabaseStatic.static_player.right
		self.collEvent2()
	
	def useObject(self):
		self.isClosed = not self.isClosed
	
	def getSprite(self):
		return wooddoorcloseSprite if self.isClosed else wooddooropenSprite
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(self.getSprite().convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class BirchDoorObject(WoodDoorObject):
	
	level = 1
	maxDurability = 48
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedBirchDoor,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def getSprite(self):
		return birchdoorcloseSprite if self.isClosed else birchdooropenSprite

class CactusDoorObject(WoodDoorObject):
	
	level = 1
	maxDurability = 48
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedCactusDoor,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def collEvent2(self):
		if DatabaseStatic.static_player.effectManager.getEffectIndex(CutEffect) == None:
			DatabaseStatic.static_player.effectManager.addEffect(CutEffect(3))
	
	def getSprite(self):
		return cactusdoorcloseSprite if self.isClosed else cactusdooropenSprite

class ClearCactusDoorObject(WoodDoorObject):
	
	level = 1
	maxDurability = 48
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedClearCactusDoor,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def getSprite(self):
		return clearcactusdoorcloseSprite if self.isClosed else clearcactusdooropenSprite

class WoodPlankObject(GameObject):
	
	solid = True
	level = 1
	maxDurability = 64
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedWood,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 64, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(woodPlankSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class BirchWoodPlankObject(GameObject):
	
	solid = True
	level = 1
	maxDurability = 64
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedBirchWood,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 64, False, 0
		
		self.ini()
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(birchWoodPlankSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class WoodSaplingObject(GrowableGameObject):
	
	solid = False
	level = 1
	maxDurability = 4
	production = TreeObject
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedAcorn,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.growStage, self.growCooldown, self.maxGrowStage = 0, 2000, 3
		self.durability, self.isBreaked, self.destStage = 4, False, 0
		
		self.ini()
		
		self.initialize(3, 70)
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(treeGrows[self.growStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class BirchSaplingObject(GrowableGameObject):
	
	solid = False
	level = 1
	maxDurability = 4
	production = BirchObject
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedBirchSapling,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.growStage, self.growCooldown, self.maxGrowStage = 0, 2000, 3
		self.durability, self.isBreaked, self.destStage = 4, False, 0
		
		self.ini()
		
		self.initialize(3, 70)
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(birchGrows[self.growStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class LiquidWaterObject(WaterObject):
	
	solid = False
	level = 1
	
	isBreakable = False
	instrument = AxeItem
	loot = tuple([])
	lootInfo = tuple([])
	
	def __init__(self, x, y, liquids=None, isBall = False):
		self.x = x
		self.y = y
		
		self.ini()
		
		self.isThereCollisionEvent = True
		
		self.doLiquid(int(liquids) if liquids != None else random.randint(2, 3), bool(isBall))
	
	def doLiquid(self, liquidCount, isBall = True):
		if liquidCount <= 0:
			return
		
		simpleWorld = DatabaseStatic.static_world
		dirsList = ((-32, 0), (32, 0), (0, -32), (0, 32))
		
		for dire in dirsList:
			newCoord = (self.x + dire[0], self.y + dire[1])
			
			#160*32=5120 and 5120+1=5121 (newCoord is in really coord, not blocks)
			if (newCoord[0] < 0 or newCoord[0] >= 5121) or (newCoord[1] < 0 or newCoord[1] >= 5121):
				continue
			
			if simpleWorld.locGet(newCoord[0], newCoord[1]) == None:
				forNextWaterLiquidCount = liquidCount - 1
				
				nextWater = LiquidWaterObject(newCoord[0], newCoord[1], forNextWaterLiquidCount)
				simpleWorld.locAdd(newCoord[0], newCoord[1], nextWater)
				
				if not isBall:
					liquidCount -= 1
	
	def drawXY(self, surface, playerX, playerY):
		pyg.draw.rect(surface, [0, 0, 255], [self.x - playerX + 400, self.y - playerY + 300, 32, 32])

class WorkbenchObject(GUIGameObject):
	
	solid = True
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedWorkbench,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 32, False, 0
		
		self.ini()
		
		self.guiInitialize()
		
		self.usableObject = True
	
	def useObject(self):
		DatabaseStatic.static_player.inventory.openWorkbench(self)
		DatabaseStatic.static_player.isInventoryOpen = False
	
	def developCraft(self):
		craftingResult = self.recipeList[self.selectedRecipeIndex].result.getInDropped(self.x, self.y)
		DatabaseStatic.static_world.locDroppedItems.append(craftingResult)
	
	def enter(self):
		if not self.recipeList[self.selectedRecipeIndex].possibility:
			return
		
		craftingResult = self.recipeList[self.selectedRecipeIndex].result.getInDropped(self.x, self.y)
		DatabaseStatic.static_world.locDroppedItems.append(craftingResult)
		
		pinvent = DatabaseStatic.static_player.inventory
		
		self.recipeList[self.selectedRecipeIndex].craft(pinvent.storageSection, pinvent.accessPanel)
		
		self.recipeList[self.selectedRecipeIndex].repossible(pinvent.storageSection, pinvent.accessPanel)
	
	def guiInitialize(self):
		self.recipeList = []
		self.selectedRecipeIndex = 0
		
		self.recipesText = pyg.font.Font("rsrc\\fonts\\times.ttf", 27).render(mp.localyze("Recipes"), 1, (255, 255, 255))
		self.componentsText = pyg.font.Font("rsrc\\fonts\\times.ttf", 27).render(mp.localyze("Components"), 1, (255, 255, 255))
		self.resultText = pyg.font.Font("rsrc\\fonts\\times.ttf", 27).render(mp.localyze("Result"), 1, (255, 255, 255))
	
	def guiStart(self):
		self.buttonsCooldown = 0
		self.craftbutton = pyg.image.load("rsrc\\sprites\\craftbutton.png").convert_alpha()
		
		self.recipeList.append(Recipe([WoodItem(16)], WoodenSword()))
		self.recipeList.append(Recipe([BirchWoodItem(16)], WoodenSword()))
		self.recipeList.append(Recipe([WoodItem(8)], WoodenPickaxe()))
		self.recipeList.append(Recipe([BirchWoodItem(8)], WoodenPickaxe()))
		self.recipeList.append(Recipe([WoodItem(12)], WoodenAxe()))
		self.recipeList.append(Recipe([BirchWoodItem(12)], WoodenAxe()))
		self.recipeList.append(Recipe([WoodItem(20)], WorkbenchItem()))
		self.recipeList.append(Recipe([BirchWoodItem(20)], BirchWorkbenchItem()))
		self.recipeList.append(Recipe([WoodItem(20)], ChestItem()))
		self.recipeList.append(Recipe([BirchWoodItem(20)], BirchChestItem()))
		self.recipeList.append(Recipe([ClearCactusItem(20)], ClearCactusChestItem()))
		self.recipeList.append(Recipe([CactusItem(20)], CactusChestItem()))
		self.recipeList.append(Recipe([CactusItem(2)], ClearCactusItem()))
		self.recipeList.append(Recipe([WoodItem(30)], CoffinItem()))
		self.recipeList.append(Recipe([BirchWoodItem(30)], CoffinItem()))
		self.recipeList.append(Recipe([WoodItem(6)], TableItem()))
		self.recipeList.append(Recipe([BirchWoodItem(6)], BirchTableItem()))
		self.recipeList.append(Recipe([ClearCactusItem(6)], ClearCactusTableItem()))
		self.recipeList.append(Recipe([CactusItem(6)], CactusTableItem()))
		self.recipeList.append(Recipe([WoodItem(4)], ChairItem()))
		self.recipeList.append(Recipe([BirchWoodItem(4)], BirchChairItem()))
		self.recipeList.append(Recipe([ClearCactusItem(4)], ClearCactusChairItem()))
		self.recipeList.append(Recipe([CactusItem(4)], CactusChairItem()))
		self.recipeList.append(Recipe([WoodItem(2)], WoodLinoleumItem()))
		self.recipeList.append(Recipe([BirchWoodItem(2)], BirchLinoleumItem()))
		self.recipeList.append(Recipe([ClearCactusItem(2)], ClearCactusLinoleumItem()))
		self.recipeList.append(Recipe([CactusItem(2)], CactusLinoleumItem()))
		self.recipeList.append(Recipe([WoodItem(15)], WoodDoorItem()))
		self.recipeList.append(Recipe([BirchWoodItem(15)], BirchDoorItem()))
		self.recipeList.append(Recipe([ClearCactusItem(15)], ClearCactusDoorItem()))
		self.recipeList.append(Recipe([CactusItem(15)], CactusDoorItem()))
		
		self.recipeList[self.selectedRecipeIndex].repossible(DatabaseStatic.static_player.inventory.storageSection, DatabaseStatic.static_player.inventory.accessPanel)
	
	def guiUpdate(self):
		if self.buttonsCooldown < 20:
			self.buttonsCooldown += 5 if pyg.key.get_pressed()[pyg.K_LCTRL] else 1
			return
		
		self.buttonsCooldown = 0
		
		if pyg.key.get_pressed()[pyg.K_z]:
			self.selectedRecipeIndex -= 1 if self.selectedRecipeIndex > 0 else 0
			self.recipeList[self.selectedRecipeIndex].repossible(DatabaseStatic.static_player.inventory.storageSection, DatabaseStatic.static_player.inventory.accessPanel)
		elif pyg.key.get_pressed()[pyg.K_x]:
			self.selectedRecipeIndex += 1 if self.selectedRecipeIndex < len(self.recipeList)-1 else 0
			self.recipeList[self.selectedRecipeIndex].repossible(DatabaseStatic.static_player.inventory.storageSection, DatabaseStatic.static_player.inventory.accessPanel)
	
	def guiDraw(self, surface, mouseX, mouseY):
		color = (0, 255, 0) if self.recipeList[self.selectedRecipeIndex].possibility else (255, 0, 0)
		
		pyg.draw.line(surface, color, (10, 470), (790, 470), 4)
		
		pyg.draw.rect(surface, (0, 0, 177), (174, 70, 452, 452))
		pyg.draw.rect(surface, (0, 0, 63), (174, 70, 452, 452), 8)
		
		#Recipes Drawing
		start_top_x, inLineRecipes = 204, 10
		top_x, top_y = start_top_x, 100
		
		startForIndex = (self.selectedRecipeIndex//inLineRecipes)*inLineRecipes
		for i in range(startForIndex, startForIndex + 100):
			try:
				if self.selectedRecipeIndex != i:
					self.recipeList[i].draw(top_x, top_y, surface)
				else:
					self.recipeList[i].drawAsSelected(top_x, top_y, surface)
				
				if i != 0 and (i + 1) % inLineRecipes == 0:
					top_x, top_y = start_top_x, top_y + 40
				else:
					top_x += 40
			except IndexError:
				break
		
		surface.blit(self.recipesText, (174 + (452 - self.recipesText.get_width()) / 2, 69))
		
		surface.blit(self.componentsText, (10, 90))
		surface.blit(self.resultText, (651, 90))
		
		pyg.draw.line(surface, color, (10, 130), (160, 130), 4)
		pyg.draw.line(surface, color, (651, 130), (790, 130), 4)
		
		components = self.recipeList[self.selectedRecipeIndex].items
		
		c_top_x, c_top_y = 10, 150
		
		for i in range(len(components)):
			self.recipeList[self.selectedRecipeIndex].drawItem(surface, c_top_x, c_top_y, i)
			if (i + 1) % 3 == 0:
				c_top_x = 10
				c_top_y += 40
			else:
				c_top_x += 40
		
		textNumber = str(self.selectedRecipeIndex + 1) + "/" + str(len(self.recipeList))
		text = pyg.font.Font("rsrc\\fonts\\times.ttf", 24).render(textNumber, 1, (255, 255, 255))
		surface.blit(text, (374, 490))
		
		surface.blit(self.craftbutton, (312, 535))
		
		self.recipeList[self.selectedRecipeIndex].drawAsSelected(700, 150, surface)
		
		self.recipeList[self.selectedRecipeIndex].drawName(634, 200, surface)
	
	def guiClose(self):
		self.recipeList = []
		self.selectedRecipeIndex = 0
		
		del self.craftbutton
		
		del self.buttonsCooldown
	
	def guiUninitialize(self):
		del self.recipeList
		del self.selectedRecipeIndex
		
		del self.recipesText
		del self.componentsText
		del self.resultText
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(workbenchSprite.convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300, 32, 32])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class BirchWorkbenchObject(WorkbenchObject):
	
	solid = True
	level = 1
	maxDurability = 32
	
	isBreakable = True
	instrument = AxeItem
	loot = (DroppedBirchWorkbench,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(birchworkbenchSprite, [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class ChestObject(GUIGameObject):
	
	solid = True
	level = 1
	maxDurability = 32
	
	instrument = AxeItem
	loot = (DroppedChest,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.durability, self.isBreaked, self.destStage = 32, False, 0
		
		self.ini()
		
		self.guiInitialize()
		
		self.isBreakable = True
		self.isThereCollisionEvent = True
		self.usableObject = True
	
	def useObject(self):
		DatabaseStatic.static_player.inventory.openWorkbench(self)
		DatabaseStatic.static_player.isInventoryOpen = False
	
	def isMatched(self, instrument):
		return self.thisStorage.isClear() and self.cursor == None and (not DatabaseStatic.static_player.inventory.isWorkbenchOpened) and GameObject.isMatched(self, instrument)
	
	def guiInitialize(self):
		self.width, self.height = 10, 4
		
		self.cursor = None
		
		self.thisStorage = DatabaseStatic.static_chest_storage()
	
	def guiStart(self):
		self.text = pyg.font.Font("rsrc\\fonts\\times.ttf", 28).render(mp.localyze("Storage"), 1, (255, 255, 255))
	
	def enter(self):
		mpos = pyg.mouse.get_pos()
		playerInventory = DatabaseStatic.static_player.inventory
		
		if playerInventory.storageSection.mouseOn(mpos[0], mpos[1]):
			slotPos = playerInventory.storageSection.getPosOnMouse(mpos[0], mpos[1])
			self.cursor = playerInventory.storageSection.swap(self.cursor, slotPos)
		elif self.thisStorage.mouseOn(mpos[0], mpos[1]):
			slotPos = self.thisStorage.getPosOnMouse(mpos[0], mpos[1])
			self.cursor = self.thisStorage.swap(self.cursor, slotPos)
	
	def guiDraw(self, surface, mouseX, mouseY):
		DatabaseStatic.static_player.inventory.storageSection.draw(surface)
		self.thisStorage.draw(surface)
		
		if self.cursor == None:
			if DatabaseStatic.static_player.inventory.storageSection.mouseOn(mouseX, mouseY):
				slotPos = DatabaseStatic.static_player.inventory.storageSection.getPosOnMouse(mouseX, mouseY)
				slot = DatabaseStatic.static_player.inventory.storageSection.getItem(slotPos[0], slotPos[1])
				if slot.item != None:
					slot.item.drawTitles(mouseX, mouseY, surface)
			elif self.thisStorage.mouseOn(mouseX, mouseY):
				slotPos = self.thisStorage.getPosOnMouse(mouseX, mouseY)
				slot = self.thisStorage.getItem(slotPos[0], slotPos[1])
				if slot.item != None:
					slot.item.drawTitles(mouseX, mouseY, surface)
		
		if self.cursor != None:
			mpos = pyg.mouse.get_pos()
			surface.blit(self.cursor.getSprite(), (mpos[0], mpos[1]))
		
		surface.blit(self.text, (10, 215))
	
	def guiClose(self):
		del self.text
	
	def guiUninitialize(self):
		del self.width
		del self.height
		del self.cursor
		del self.thisStorage
	
	def doCollsiion(self):
		pass
	
	def getSprite(self):
		return woodchestSprite
	
	def drawXY(self, surface, playerX, playerY):
		surface.blit(self.getSprite(), [self.x - playerX + 400, self.y - playerY + 300])
		if self.destStage != 0:
			surface.blit(damages[self.destStage].convert_alpha(), [self.x - playerX + 400, self.y - playerY + 300])

class BirchChestObject(ChestObject):
	
	solid = True
	level = 1
	maxDurability = 32
	
	instrument = AxeItem
	loot = (DroppedBirchChest,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def getSprite(self):
		return birchchestSprite

class CactusChestObject(ChestObject):
	
	solid = True
	level = 1
	maxDurability = 32
	
	instrument = AxeItem
	loot = (DroppedCactusChest,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def doCollsiion(self):
		if DatabaseStatic.static_player.effectManager.getEffectIndex(CutEffect) == None:
			DatabaseStatic.static_player.effectManager.addEffect(CutEffect(3))
	
	def getSprite(self):
		return cactuschestSprite

class ClearCactusChestObject(ChestObject):
	
	solid = True
	level = 1
	maxDurability = 32
	
	instrument = AxeItem
	loot = (DroppedClearCactusChest,)
	lootInfo = ((lambda: True, 1, 1),)
	
	def getSprite(self):
		return clearcactuschestSprite