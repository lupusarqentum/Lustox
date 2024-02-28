import pygame as pyg

class GameSprite:
	
	def __init__(self, sprite):
		self.sprite = sprite
	
	def getSprite(self):
		return self.sprite

class SpriteAnimation:
	
	def __init__(self, sprites, frames, frameDelay):
		self.sprites = sprites
		self.frames = frames
		self.frameDelay = frameDelay
		self.tempFrame = 0
		self.tempDelay = 0
	
	def getSprite(self):
		rt = self.sprites[self.tempFrame]
		if self.tempDelay >= self.frameDelay:
			self.tempDelay = 0
			self.tempFrame += 1
		else:
			self.tempDelay += 1
		if self.tempFrame >= self.frames:
			self.tempFrame = 0
		return rt

def rotateAnim(anim, angle):
	newSprites = list(anim.sprites)
	for i in range(len(newSprites)):
		newSprites[i] = pyg.transform.rotate(newSprites[i], angle)
	newAnim = SpriteAnimation(newSprites, anim.frames, anim.frameDelay)
	return newAnim