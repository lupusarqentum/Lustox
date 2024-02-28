import pygame as pyg

class EffectManager:
	
	def __init__(self):
		self.effects = []
	
	def clearEffects(self):
		self.effects = []
	
	def getEffectIndex(self, effectType):
		for i in range(len(self.effects)):
			if type(self.effects[i]) == effectType:
				return i
		return None
	
	def addEffect(self, effect):
		for eff in self.effects:
			if type(eff) == type(effect):
				eff.timeSec += effect.timeSec
				break
		else:
			self.effects.append(effect)
	
	def removeEffect(self, index):
		del self.effects[index]
	
	def update(self, player):
		for i in range(len(self.effects)):
			try:
				self.effects[i].update(player)
				if self.effects[i].isEnded:
					self.removeEffect(i)
			except IndexError:
				pass
	
	def draw(self, surface):
		topMargin = 50
		leftMargin = 8
		for i in range(len(self.effects)):
			self.effects[i].draw(surface, leftMargin, topMargin)
			if i != 0 and (i + 1) % 8 == 0:
				leftMargin = 8
				topMargin += 45
			else:
				leftMargin += 40