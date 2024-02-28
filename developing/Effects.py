import pygame as pyg
import datetime
import random

times_font = pyg.font.Font("rsrc\\fonts\\times.ttf", 13)

class Effect:
	
	def __init__(self):
		self.icon = None
		self.isEnded = False
		self.timeSec = 60
		self.lastSec = datetime.datetime.now().second
	
	def update(self, player):
		self.realUpdate(player)
		sec = datetime.datetime.now().second
		if sec != self.lastSec:
			self.tick(player)
			self.lastSec = sec
			del sec
			self.timeSec -= 1
			if self.timeSec == -1:
				self.timeSec = 0
				self.isEnded = True
				self.endOfEffect(player)
	
	def tick(self, player):
		pass
	
	def realUpdate(self, player):
		pass
	
	def endOfEffect(self, player):
		pass
	
	def draw(self, surface, x, y):
		pyg.draw.rect(surface, (0, 0, 255), (x, y, 32, 32))
		pyg.draw.rect(surface, (0, 0, 177), (x, y, 32, 32), 2)
		surface.blit(self.icon, (x, y))
		
		toBlit = times_font.render(str(self.timeSec), 1, (255, 255, 255))
		surface.blit(toBlit, ((32-toBlit.get_width())/2+x, 24+y))

class HealingDelayEffect(Effect):
	
	def __init__(self, timeSec):
		self.icon = pyg.image.load("rsrc\\icons\\afterheal.png").convert_alpha()
		self.isEnded = False
		self.timeSec = timeSec
		self.lastSec = datetime.datetime.now().second

class HpRestoreEffect(Effect):
	
	def __init__(self, timeSec):
		self.icon = pyg.image.load("rsrc\\icons\\hprestore.png").convert_alpha()
		self.isEnded = False
		self.timeSec = timeSec
		self.lastSec = datetime.datetime.now().second
	
	def tick(self, player):
		player.hp += 2 if player.hp < player.maxHp else 0

class HpRestoreEffect2(Effect):
	
	def __init__(self, timeSec):
		self.icon = pyg.image.load("rsrc\\icons\\hprestore.png").convert_alpha()
		self.isEnded = False
		self.timeSec = timeSec
		self.lastSec = datetime.datetime.now().second
	
	def tick(self, player):
		player.hp += 4 if player.hp < player.maxHp else 0

class CutEffect(Effect):
	
	def __init__(self, timeSec):
		self.icon = pyg.image.load("rsrc\\icons\\cut.png").convert_alpha()
		self.isEnded = False
		self.timeSec = timeSec
		self.lastSec = datetime.datetime.now().second
	
	def tick(self, player):
		player.hp -= (6 if player.hp > 0 else 0)
		
		if player.hp < 0:
			player.hp = 0
	
	def endOfEffect(self, player):
		damage = 10
		if player.hp > damage:
			player.hp -= damage
		else:
			player.hp = 0

class CutEffect2(Effect):
	
	def __init__(self, timeSec):
		self.icon = pyg.image.load("rsrc\\icons\\cut2.png").convert_alpha()
		self.isEnded = False
		self.timeSec = timeSec
		self.lastSec = datetime.datetime.now().second
	
	def tick(self, player):
		player.hp -= (random.randint(7, 13) if player.hp > 0 else 0)
		
		if player.hp < 0:
			player.hp = 0
	
	def endOfEffect(self, player):
		damage = 30
		if player.hp > damage:
			player.hp -= damage
		else:
			player.hp = 0

class ImmunityEffect(Effect):
	
	def __init__(self, timeSec):
		self.icon = pyg.image.load("rsrc\\icons\\immunity.png").convert_alpha()
		self.isEnded = False
		self.timeSec = timeSec
		self.lastSec = datetime.datetime.now().second
	
	def tick(self, player):
		if player.hp < player.maxHp:
			player.hp = player.maxHp