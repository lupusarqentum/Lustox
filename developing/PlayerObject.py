import pygame as pyg
import random
import math
import json
from pygame.locals import *

import MPlayer as mp
from Inventory import *
from SpriteAnimation import *
from Effects import *
#from Items import *
from EffectManager import EffectManager
from StaticData import DatabaseStatic

class Tip:
	
	def __init__(self, x, y, value, color, maxTimes, size = 36):
		self.x, self.y = x, y
		self.maxTimes, self.times = maxTimes, 0
		tipFont = pyg.font.Font("rsrc\\fonts\\times.ttf", size)
		self.value = tipFont.render(str(value), 1, color)
		self.textValue = value
	
	def draw(self, surface, playerX, playerY):
		surface.blit(self.value, [self.x - playerX + 400, self.y - playerY + 300])

class PlayerObject(GameObject):
	
	NormalGo = 2
	SuperGo = 12
	ItemTipSize = 18
	
	def __init__(self, x, y):
		self.x, self.y, self.xPrevious, self.yPrevious = x, y, x, y
		self.moveSpeed = PlayerObject.NormalGo
		self.maxHp, self.maxMana = 100, 100
		self.hp, self.mana = 100, 100
		self.left, self.right, self.up, self.down = False, False, False, False
		self.hpCooldown = 0
		self.isDead, self.heartbeatPlaying, self.isInventoryOpen = False, False, False
		self.inventory = Inventory()
		self.buildRad = 96
		self.tips = []
		self.itemTips = []
		self.message, self.messageCooldown = "", 132
		self.isShip = False
		self.waterSprays = []
		self.sprayCooldown = 60
		
		self.loadContent()
		
		self.textAboutCoordinates = self.guiFont.render(("(%04d, %04d)" % (self.x, self.y)), 1, [0, 0, 0])
		
		jsonLoaded = open("settings.json", 'r')
		data = json.load(jsonLoaded)
		jsonLoaded.close()
		self.particlesLevel = data["particles"]
		
		self.effectManager = EffectManager()
		
		self.effectManager.addEffect(ImmunityEffect(2))
		
		DatabaseStatic.static_player_tip = Tip
	
	def loadContent(self):
		#Font
		self.guiFont = pyg.font.Font("rsrc\\fonts\\times.ttf", 24)
		
		#Texts
		self.sLetter = self.guiFont.render(mp.localyze("S"), 1, [0, 0, 0])
		self.saveWord = self.guiFont.render(mp.localyze("Save"), 1, [0, 0, 0])
		
		#Animation Spped
		frameSpeed = 11
		
		#Player Sprites
		
		s_playergoup1 = pyg.image.load("rsrc\\sprites\\playergoup1.png")
		s_playergodown1 = pyg.image.load("rsrc\\sprites\\playergodown1.png")
		s_playergoleft1 = pyg.image.load("rsrc\\sprites\\playergoleft1.png")
		s_playergoright1 = pyg.image.load("rsrc\\sprites\\playergoright1.png")
		s_playergoup2 = pyg.image.load("rsrc\\sprites\\playergoup2.png")
		s_playergodown2 = pyg.image.load("rsrc\\sprites\\playergodown2.png")
		s_playergoleft2 = pyg.image.load("rsrc\\sprites\\playergoleft2.png")
		s_playergoright2 = pyg.image.load("rsrc\\sprites\\playergoright2.png")
		
		s_playerseeup = pyg.image.load("rsrc\\sprites\\playerup.png")
		s_playerseedown = pyg.image.load("rsrc\\sprites\\playerdown.png")
		s_playerseeleft = pyg.image.load("rsrc\\sprites\\playerleft.png")
		s_playerseeright = pyg.image.load("rsrc\\sprites\\playerright.png")
		
		self.a_playergoup = SpriteAnimation([s_playergoup1, s_playergoup2], 2, frameSpeed)
		self.a_playergodown = SpriteAnimation([s_playergodown1, s_playergodown2], 2, frameSpeed)
		self.a_playergoleft = SpriteAnimation([s_playergoleft1, s_playergoleft2], 2, frameSpeed)
		self.a_playergoright = SpriteAnimation([s_playergoright1, s_playergoright2], 2, frameSpeed)
		
		self.a_playerseeup = GameSprite(s_playerseeup)
		self.a_playerseedown = GameSprite(s_playerseedown)
		self.a_playerseeleft = GameSprite(s_playerseeleft)
		self.a_playerseeright = GameSprite(s_playerseeright)
		
		self.sprite = self.a_playerseedown
		
		#Ship sprites
		self.a_shipHorizontal = GameSprite(pyg.image.load("rsrc\\sprites\\ship.png"))
		self.a_shipVertical = GameSprite(pyg.transform.rotate(self.a_shipHorizontal.getSprite(), 90))
		
		self.shipSprite = self.a_shipHorizontal
	
	def respawn(self):
		self.x = 2560
		self.y = 2560
		self.moveSpeed = PlayerObject.NormalGo
		self.hp, self.mana = self.maxHp, self.maxMana
		self.left, self.right, self.up, self.down = False, False, False, False
		self.hpCooldown = 0
		self.isDead, self.heartbeatPlaying, self.isInventoryOpen = False, False, False
		self.inventory.closeWorkbench()
		self.sprite = self.a_playerseedown
		self.tips = []
		self.shipSprite = self.a_shipHorizontal
		self.isShip = False
		self.waterSprays = []
		self.sprayCooldown = 60
		self.itemTips = []
		jsonLoaded = open("settings.json", 'r')
		data = json.load(jsonLoaded)
		jsonLoaded.close()
		self.particlesLevel = data["particles"]
		
		self.effectManager.clearEffects()
		self.effectManager.addEffect(ImmunityEffect(2))
	
	def sendMessage(self, message, cooldown = 528):
		self.message = message
		self.messageCooldown = cooldown
	
	def objectUsing(self, other):
		#if object is far from player return this method
		if math.sqrt( (self.x - other.x) ** 2 + (self.y - other.y) ** 2) > self.buildRad:
			return
		
		if other != None and other.usableObject:
			other.useObject()
	
	def collisionEvent(self, other):
		if other.isThereCollisionEvent:
			other.doCollsiion()
			if other.solid:
				if self.up:
					self.y += self.moveSpeed
				if self.down:
					self.y -= self.moveSpeed
				if self.left:
					self.x += self.moveSpeed
				if self.right:
					self.x -= self.moveSpeed
		elif other.solid:
			if self.up:
				self.y += self.moveSpeed
			if self.down:
				self.y -= self.moveSpeed
			if self.left:
				self.x += self.moveSpeed
			if self.right:
				self.x -= self.moveSpeed
		elif isinstance(other, DroppedItem):
			unfailedPutting = self.inventory.putOn(other.item)
			if unfailedPutting:
				tipText = other.item.itemName + "(" + str(other.item.count) + ")"
				newItemTip = Tip(400, 276, tipText, (255, 255, 255), 120, self.ItemTipSize)
				newItemTip.x = 400 - newItemTip.value.get_width()/2 + 16
				newItemTip.y = 284
				self.itemTips.insert(0, newItemTip)
				for i in range(1, len(self.itemTips)):
					self.itemTips[i].y -= self.ItemTipSize
				if len(self.itemTips) > 9:
					del self.itemTips[len(self.itemTips) - 1]
	
	def eventClickOn(self, other):
		selectedSlot = self.inventory.accessPanel.getSelectedSlot().item
		
		if type(other) == SandObject and isinstance(selectedSlot, (PickaxeItem, CactusItem, AxeItem)):
			if isinstance(selectedSlot, PickaxeItem) and other.on == None:
				if other.isMatched(selectedSlot):	
					if math.sqrt( (self.x - other.x) ** 2 + (self.y - other.y) ** 2) <= selectedSlot.radius:
						other.destroy(selectedSlot.power, selectedSlot.level)
						if other.isBreaked:
							other.getLoot()
			elif isinstance(selectedSlot, CactusItem) and other.on == None:
				if math.sqrt( (self.x - other.x) ** 2 + (self.y - other.y) ** 2) <= self.buildRad:
					other.setOn(CactusSaplingObject(other.x, other.y))
					self.inventory.accessPanel.minus()
			elif other.on != None and isinstance(selectedSlot, AxeItem):
				self.eventClickOn(other.on)
		elif type(other) == CactusObject and isinstance(selectedSlot, AxeItem):
			if other.isMatched(selectedSlot):	
				if math.sqrt( (self.x - other.x) ** 2 + (self.y - other.y) ** 2) <= selectedSlot.radius:
					other.destroy(selectedSlot.power, selectedSlot.level)
					if other.isBreaked:
						other.getLoot()
						DatabaseStatic.static_world.locGet(other.x, other.y).setOn(None)
		elif type(other) == CactusSaplingObject and isinstance(selectedSlot, AxeItem):
			if other.isMatched(selectedSlot):	
				if math.sqrt( (self.x - other.x) ** 2 + (self.y - other.y) ** 2) <= selectedSlot.radius:
					other.destroy(selectedSlot.power, selectedSlot.level)
					if other.isBreaked:
						other.getLoot()
						DatabaseStatic.static_world.locGet(other.x, other.y).setOn(None)
		elif other.isMatched(selectedSlot):
			if math.sqrt( (self.x - other.x) ** 2 + (self.y - other.y) ** 2) <= selectedSlot.radius:
				other.destroy(selectedSlot.power, selectedSlot.level)
				if other.isBreaked:
					other.getLoot()
			else:
				self.useItem()
		else:
			self.useItem()
	
	def useItem(self):
		selectedItem = self.inventory.accessPanel.getSelectedSlot().item
		
		if selectedItem != None and selectedItem.usableItem:
			selectedItem.useItem()
	
	def clickOnScreen(self, mouseX, mouseY):
		mouseX = (mouseX // 32) * 32
		mouseY = (mouseY // 32) * 32
		
		if math.sqrt( (self.x - mouseX) ** 2 + (self.y - mouseY) ** 2) > self.buildRad:
			self.useItem()
			return None
		elif abs(self.x - mouseX) < 32 and abs(self.y - mouseY) < 32:
			self.useItem()
			return None
		elif mouseX < 0 or mouseX > 5120 or mouseY < 0 or mouseY > 5120:
			self.useItem()
			return None
		elif DatabaseStatic.static_world.locGet(mouseX, mouseY) != None:
			self.useItem()
			return None
		
		selectedItem = self.inventory.accessPanel.getSelectedSlot().item
		
		if selectedItem != None and selectedItem.putObject != None:
			obj = selectedItem.putObject(mouseX, mouseY)
			self.inventory.accessPanel.minus()
			return obj
		
		self.useItem()
		return None
	
	def update(self, params):
		# Every timer tick doing
		if params == None:
			#Heartbeat Playing
			if self.hp < 10:
				mp.playSound(mp.GameSounds.heartbeat)
				self.heartbeatPlaying = True
			elif self.heartbeatPlaying:
				mp.stopSound(mp.GameSounds.heartbeat)
				self.heartbeatPlaying = False
			
			#Effects Update
			self.effectManager.update(self)
			
			#collision event will be called after update-call.
			#choice of ship or normal sprite updating
			self.isShip = False
			
			#Update water sprays
			for i in range(len(self.waterSprays)):
				self.waterSprays[i].update()
				if self.waterSprays[i].lifeTimeFrames < 1:
					self.waterSprays[i] = None
			
			while None in self.waterSprays:
				self.waterSprays.remove(None)
			
			#Update of workbench, furnance, anvil interface
			if self.inventory.isWorkbenchOpened:
				self.inventory.update(self.x, self.y, self.buildRad)
			
			# Message cleaning
			if self.message != "":
				self.messageCooldown -= 1
				if self.messageCooldown == 0:
					self.message = ""
					self.messageCooldown = 132
			
			# to movement
			self.left, self.right, self.up, self.down = False, False, False, False
			
			#Player is dead if hp equals 0
			if self.hp == 0:
				self.isDead = True
			
			#HP Restoring
			if self.hp < self.maxHp:
				self.hpCooldown += 1
				if self.hpCooldown == 50:
					self.hp += 1
					self.hpCooldown = 0
			
			#Removing useless tips
			needDeleting = False
			for i in range(len(self.tips)):
				self.tips[i].times += 1
				if self.tips[i].times == self.tips[i].maxTimes:
					self.tips[i] = None
					needDeleting = True
			if needDeleting:
				while None in self.tips:
					self.tips.remove(None)
			del needDeleting
			
			#Removing useless item tips
			needDeleting = False
			for i in range(len(self.itemTips)):
				self.itemTips[i].times += 1
				if self.itemTips[i].times >= self.itemTips[i].maxTimes:
					self.itemTips[i] = None
					needDeleting = True
			if needDeleting:
				while None in self.itemTips:
					self.itemTips.remove(None)
			del needDeleting
			
			#If params is None next statements is useless. So, return this method.
			return
		
		#Player and ship Moving
		if params in ("up", "down", "left", "right"):
			if params == "up":
				#Moving to up
				self.y -= self.moveSpeed
				if self.sprite != self.a_playergoup:
					self.sprite = self.a_playergoup
				self.up = True
				if self.y <= 0:
					self.y += self.moveSpeed
					self.sprite = self.a_playerseeup
				self.textAboutCoordinates = self.guiFont.render(("(%04d, %04d)" % (self.x, self.y)), 1, [0, 0, 0])
			elif params == "down":
				#Moving to down
				self.y += self.moveSpeed
				if self.sprite != self.a_playergodown:
					self.sprite = self.a_playergodown
				self.down = True
				if self.y >= 5120:
					self.y -= self.moveSpeed
					self.sprite = self.a_playerseedown
				self.textAboutCoordinates = self.guiFont.render(("(%04d, %04d)" % (self.x, self.y)), 1, [0, 0, 0])
			elif params == "left":
				#Moving to left
				self.x -= self.moveSpeed
				if self.sprite != self.a_playergoleft:
					self.sprite = self.a_playergoleft
				self.left = True
				if self.x <= 0:
					self.x += self.moveSpeed
					self.sprite = self.a_playerseeleft
				self.textAboutCoordinates = self.guiFont.render(("(%04d, %04d)" % (self.x, self.y)), 1, [0, 0, 0])
			else:
				#Moving to right
				self.x += self.moveSpeed
				if self.sprite != self.a_playergoright:
					self.sprite = self.a_playergoright
				self.right = True
				if self.x >= 5120:
					self.x -= self.moveSpeed
					self.sprite = self.a_playerseeright
				self.textAboutCoordinates = self.guiFont.render(("(%04d, %04d)" % (self.x, self.y)), 1, [0, 0, 0])
			return
		
		#Inventory mouse clicks update
		if params.type == MOUSEBUTTONDOWN:
			if params.button in [4, 5]:
				self.inventory.mouseEvent(0, 0, params.button)
			elif self.isInventoryOpen:
				self.mouseButton(params)
			elif self.inventory.accessPanel.mouseOn(params.pos[0], params.pos[1]):
				slotX = self.inventory.accessPanel.getPosOnMouse(params.pos[0], params.pos[1])
				self.inventory.accessPanel.selectedSlotX = slotX
		elif params.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0]:
			#Change hotbar slot
			if params.key == K_1:
				self.inventory.accessPanel.selectedSlotX = 0
			elif params.key == K_2:
				self.inventory.accessPanel.selectedSlotX = 1
			elif params.key == K_3:
				self.inventory.accessPanel.selectedSlotX = 2
			elif params.key == K_4:
				self.inventory.accessPanel.selectedSlotX = 3
			elif params.key == K_5:
				self.inventory.accessPanel.selectedSlotX = 4
			elif params.key == K_6:
				self.inventory.accessPanel.selectedSlotX = 5
			elif params.key == K_7:
				self.inventory.accessPanel.selectedSlotX = 6
			elif params.key == K_8:
				self.inventory.accessPanel.selectedSlotX = 7
			elif params.key == K_9:
				self.inventory.accessPanel.selectedSlotX = 8
			elif params.key == K_0:
				self.inventory.accessPanel.selectedSlotX = 9
		elif params.type in [KEYUP, KEYDOWN] and params.key == K_q:
			#Items dropping
			if self.isInventoryOpen:
				#Coords where item will be dropped
				xCoord, yCoord = None, None
				#X Calculating
				if self.x > 32:
					xCoord = self.x - 32
				else:
					xCoord = self.x + 32
				#Y Calculating
				if self.y > 32:
					yCoord = self.y - 32
				else:
					yCoord = self.y + 32
				#Get item to drop
				oDropped = self.inventory.drop(pyg.mouse.get_pos()[0], pyg.mouse.get_pos()[1], xCoord, yCoord)
				#Drop item
				if oDropped != None:
					DatabaseStatic.static_world.locAdd(oDropped.x, oDropped.y, oDropped)
		elif params.type == KEYUP and params.key == K_i:
			#Inventory opening
			self.isInventoryOpen = not self.isInventoryOpen
			
			#Workbench Closing
			if self.inventory.isWorkbenchOpened:
				self.inventory.closeWorkbench()
		elif params.type == KEYDOWN and params.key == K_o:
			#SuperFast on
			self.moveSpeed = PlayerObject.SuperGo
		elif params.type == KEYUP and params.key == K_o:
			#SuperFast off
			self.moveSpeed = PlayerObject.NormalGo
		elif params.type in [KEYUP, KEYDOWN] and params.key == K_y:
			#Teleport to center of world
			self.x = 2560
			self.y = 2560
		elif params.type == KEYDOWN and params.key == K_w:
			#Sprite Changing
			self.sprite = self.a_playergoup
		elif params.type == KEYDOWN and params.key == K_s:
			#Sprite Changing
			self.sprite = self.a_playergodown
		elif params.type == KEYDOWN and params.key == K_a:
			#Sprite Changing
			self.sprite = self.a_playergoleft
		elif params.type == KEYDOWN and params.key == K_d:
			#Sprite Changing
			self.sprite = self.a_playergoright
		elif params.type == KEYUP and params.key in [K_w, K_UP]:
			#Sprite Changing
			self.sprite = self.a_playerseeup
		elif params.type == KEYUP and params.key in [K_a, K_LEFT]:
			#Sprite Changing
			self.sprite = self.a_playerseeleft
		elif params.type == KEYUP and params.key in [K_s, K_DOWN]:
			#Sprite Changing
			self.sprite = self.a_playerseedown
		elif params.type == KEYUP and params.key in [K_d, K_RIGHT]:
			#Sprite Changing
			self.sprite = self.a_playerseeright
	
	def mouseButton(self, event):
		mousePos = event.pos
		self.inventory.mouseEvent(mousePos[0], mousePos[1], event.button)
	
	def drawHealthbar(self, surface, value, x, y, color, width, height):
		pyg.draw.rect(surface, [0, 0, 0], [x - 2, y - 2, width + 4, height + 4])
		pyg.draw.rect(surface, color, [x, y, value * 2, height])
	
	def draw(self, surface, mouseX, mouseY):
		
		if self.left or self.right or ((not self.up) and (not self.down)):
			self.shipSprite = self.a_shipHorizontal
		else:
			self.shipSprite = self.a_shipVertical
		
		for spray in self.waterSprays:
			spray.draw(surface, self.x, self.y)
		
		for t in self.tips:
			t.draw(surface, self.x, self.y)
		
		for t in self.itemTips:
			t.draw(surface, 400, 300)
		
		self.drawHealthbar(surface, self.hp / (self.maxHp / 100), 575, 30, [255, 0, 0], 200, 25)
		self.drawHealthbar(surface, self.mana / (self.maxMana / 100), 575, 65, [0, 0, 255], 200, 25)
		
		textAboutHp = self.guiFont.render(mp.localyze("Hp: ") + str(self.hp) + "/" + str(self.maxHp), 1, [255, 255, 255])
		textAboutMana = self.guiFont.render(mp.localyze("Mana: ") + str(self.mana) + "/" + str(self.maxMana), 1, [255, 255, 255])
		
		surface.blit(textAboutHp, [583, 33])
		surface.blit(textAboutMana, [583, 68])
		
		surface.blit(self.textAboutCoordinates, [375, 30])
		
		pyg.draw.rect(surface, [127, 127, 127], [540, 30, 32, 32])
		surface.blit(self.sLetter, [545, 35])
		
		pyg.draw.rect(surface, [127, 127, 127], [522, 65, 50, 30])
		surface.blit(self.saveWord, [522, 70])
		
		if not self.isShip:
			surface.blit(self.sprite.getSprite(), [400, 300])
		else:
			surface.blit(self.shipSprite.getSprite(), [400, 300])
		
		messageText = self.guiFont.render(self.message, 1, [0, 0, 0])
		
		surface.blit(messageText, [30, 550])
		
		if self.isInventoryOpen:
			self.inventory.draw(surface, mouseX, mouseY)
		else:
			self.inventory.drawAccessPanel(surface)
			
			if not self.inventory.isWorkbenchOpened:
				self.effectManager.draw(surface)