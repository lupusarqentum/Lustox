import pygame as pyg
import math

from StaticData import DatabaseStatic
from Items import *

class Slot:
	
	def __init__(self, item = None):
		self.item = item
		self.font = pyg.font.Font("rsrc\\fonts\\times.ttf", 16)
	
	def getCopy(self):
		return Slot(self.item)
	
	def plusTo(self, count):
		self.item.count += count
	
	def set(self, item):
		itemCopy = self.item
		self.item = item
		return itemCopy
	
	def getAll(self):
		itemCopy = self.item
		self.item = None
		return itemCopy
	
	def getOne(self):
		if self.item.count > 1:
			self.item.count -= 1
			itemCopy = self.item.getSingleComponent()
		else:
			itemCopy = self.item
			self.item = None
		return itemCopy
	
	def isEmpty(self):
		return self.item == None
	
	def draw(self, x, y, surface):
		pyg.draw.rect(surface, [0, 0, 255], [x, y, 32, 32])
		pyg.draw.rect(surface, [0, 0, 127], [x, y, 32, 32], 3)
		if not self.isEmpty():
			surface.blit(self.item.getSprite(), [x, y])
			surface.blit(self.font.render(str(self.item.count), 1, [255, 255, 255]), [x, y])
	
	def drawSelected(self, x, y, surface):
		pyg.draw.rect(surface, [0, 0, 255], [x, y, 32, 32])
		pyg.draw.rect(surface, [255, 255, 0], [x, y, 32, 32], 2)
		if not self.isEmpty():
			surface.blit(self.item.getSprite(), [x, y])
			surface.blit(self.font.render(str(self.item.count), 1, [255, 255, 255]), [x, y])

class TrashSlot():
	
	def __init__(self):
		self.x, self.y, self.sprite = 350, 167, pyg.image.load("rsrc\\sprites\\trashcan.png")
	
	def mouseOn(self, mouseX, mouseY):
		if mouseX >= self.x and mouseX <= self.x + 32 and mouseY >= self.y and mouseY <= self.y + 32:
			return True
		return False
	
	def draw(self, surface):
		pyg.draw.rect(surface, [0, 0, 255], [self.x, self.y, 32, 32])
		pyg.draw.rect(surface, [0, 0, 127], [self.x, self.y, 32, 32], 3)
		surface.blit(self.sprite, [self.x, self.y])

class AccessPanel:
	
	def __init__(self):
		self.selectedSlotX = 0
		self.width = 10
		self.storage = []
		for i in range(self.width):
			self.storage.append(Slot())
		self.font = pyg.font.Font("rsrc\\fonts\\times.ttf", 16)
	
	def minus(self):
		return self.getSelectedSlot().getOne()
	
	def wheel(self, speed):
		self.selectedSlotX += speed
		if self.selectedSlotX > 9:
			self.selectedSlotX = 0
		elif self.selectedSlotX < 0:
			self.selectedSlotX = 9
	
	def setSelectedSlot(self, slot):
		self.storage[self.selectedSlotX] = slot
	
	def getSelectedSlot(self):
		return self.storage[self.selectedSlotX]
	
	def putOn(self, item):
		for i in range(self.width):
			try:
				logical = self.getItem(i).item.systemName == item.systemName
			except AttributeError:
				logical = False
			if logical:
				self.getItem(i).plusTo(item.count)
				return
		for i in range(self.width):
			if self.getItem(i).item == None:
				self.setItem(i, item)
				return
	
	def dropItems(self, item):
		fc = item.count
		for i in range(self.width):
			tempItem = self.getItem(i).item
			
			if tempItem == None:
				continue
			
			if tempItem.systemName == item.systemName:
				if fc >= tempItem.count:
					fc -= int(tempItem.count)
					self.setItem(i, None)
				else:
					tempItem.count -= fc
					return 0
		return fc
	
	def getItemCount(self, item):
		fc = 0
		for i in range(self.width):
			tempItem = self.getItem(i).item
			if tempItem == None:
				continue
			
			if tempItem.systemName == item.systemName:
				fc += tempItem.count
		return fc
	
	def isFreeSlotFor(self, item):
		for i in range(self.width):
			tempSlot = self.getItem(i)
			if tempSlot.item == None:
				return True
			else:
				if tempSlot.item.systemName == item.systemName:
					return True
		return False
	
	def mouseOn(self, mouseX, mouseY):
		for i in range(self.width):
			if mouseX >= i * 32 + i * 3 and mouseX <= i * 32 + i * 3 + 32 and mouseY >= 10 and mouseY <= 42:
				return True
		return False
	
	def getPosOnMouse(self, mouseX, mouseY):
		for i in range(self.width):
			if mouseX >= i * 32 + i * 3 and mouseX <= i * 32 + i * 3 + 32 and mouseY >= 10 and mouseY <= 42:
				return i
		return None
	
	def swap(self, item, x):
		try:
			logical = self.getItem(x).item.systemName != item.systemName
		except AttributeError:
			logical = True
		if logical:
			return self.getItem(x).set(item)
		else:
			cursorCount = item.count
			self.getItem(x).item.count += cursorCount
			return None
	
	def getItem(self, x):
		return self.storage[x]
	
	def setItem(self, x, item):
		self.storage[x].set(item)
	
	def draw(self, surface):
		for i in range(self.width):
			if i != self.selectedSlotX:
				self.getItem(i).draw(i * 32 + i * 3, 10, surface)
			else:
				self.getItem(i).drawSelected(i * 32 + i * 3, 10, surface)
			if i != 9:
				surface.blit(self.font.render(str(i + 1), 1, [255, 255, 255]), [i * 35 + 16, 26])
			else:
				surface.blit(self.font.render("0", 1, [255, 255, 255]), [i * 35 + 16, 26])

class StorageSection:
	
	def __init__(self):
		self.width = 10
		self.height = 4
		self.storage = []
		for i in range(self.height):
			timeList = []
			for j in range(self.width):
				timeList.append(Slot())
			self.storage.append(timeList)
	
	def putOn(self, item):
		for i in range(self.height):
			for j in range(self.width):
				try:
					logical = self.getItem(j, i).item.systemName == item.systemName
				except AttributeError:
					logical = False
				if logical:
					self.getItem(j, i).plusTo(item.count)
					return
		for i in range(self.height):
			for j in range(self.width):
				if self.getItem(j, i).item == None:
					self.setItem(j, i, item)
					return
	
	def dropItems(self, item):
		fc = item.count
		for i in range(self.height):
			for j in range(self.width):
				tempItem = self.getItem(j, i).item
				
				if tempItem == None:
					continue
				
				if tempItem.systemName == item.systemName:
					if fc >= tempItem.count:
						fc -= int(tempItem.count)
						self.setItem(j, i, None)
					else:
						tempItem.count -= fc
						return 0
		return fc
	
	def getItemCount(self, item):
		fc = 0
		for i in range(self.height):
			for j in range(self.width):
				tempItem = self.getItem(j, i).item
				if tempItem == None:
					continue
				
				if tempItem.systemName == item.systemName:
					fc += tempItem.count
		return fc
	
	def isFreeSlotFor(self, item):
		for i in range(self.height):
			for j in range(self.width):
				tempSlot = self.getItem(j, i)
				if tempSlot.item == None:
					return True
				else:
					if tempSlot.item.systemName == item.systemName:
						return True
		return False
	
	def mouseOn(self, mouseX, mouseY):
		for i in range(self.height):
			for j in range(self.width):
				if mouseX >= j * 32 + j * 3 and mouseX <= j * 32 + j * 3 + 32 and mouseY >= i * 32 + 62 + i * 3 and mouseY <= i * 32 + 62 + i * 3 + 32:
					return True
		return False
	
	def getPosOnMouse(self, mouseX, mouseY):
		for i in range(self.height):
			for j in range(self.width):
				if mouseX >= j * 32 + j * 3 and mouseX <= j * 32 + j * 3 + 32 and mouseY >= i * 32 + 62 + i * 3 and mouseY <= i * 32 + 62 + i * 3 + 32:
					return j, i
		return None
	
	def swap(self, item, slotPos):
		try:
			logical = self.getItem(slotPos[0], slotPos[1]).item.systemName != item.systemName
		except AttributeError:
			logical = True
		if logical:
			return self.getItem(slotPos[0], slotPos[1]).set(item)
		else:
			cursorCount = item.count
			self.getItem(slotPos[0], slotPos[1]).item.count += cursorCount
			return None
	
	def getItem(self, x, y):
		return self.storage[y][x]
	
	def setItem(self, x, y, item):
		self.storage[y][x].set(item)
	
	def draw(self, surface):
		for i in range(self.height):
			for j in range(self.width):
				self.getItem(j, i).draw(j * 35, i * 35 + 62, surface)

class ChestStorage:
	
	def __init__(self):
		self.plusY = 200
		
		self.width = 10
		self.height = 4
		self.storage = []
		for i in range(self.height):
			timeList = []
			for j in range(self.width):
				timeList.append(Slot())
			self.storage.append(timeList)
	
	def isClear(self):
		for i in range(self.height):
			for j in range(self.width):
				if self.getItem(j, i).item != None:
					return False
		return True
	
	def mouseOn(self, mouseX, mouseY):
		for i in range(self.height):
			for j in range(self.width):
				if mouseX >= j * 32 + j * 3 and mouseX <= j * 32 + j * 3 + 32 and mouseY >= i * 32 + 62 + i * 3 + self.plusY and mouseY <= i * 32 + 62 + i * 3 + 32 + self.plusY:
					return True
		return False
	
	def getPosOnMouse(self, mouseX, mouseY):
		for i in range(self.height):
			for j in range(self.width):
				if mouseX >= j * 32 + j * 3 and mouseX <= j * 32 + j * 3 + 32 and mouseY >= i * 32 + 62 + i * 3 + self.plusY and mouseY <= i * 32 + 62 + i * 3 + 32 + self.plusY:
					return j, i
		return None
	
	def swap(self, item, slotPos):
		try:
			logical = self.getItem(slotPos[0], slotPos[1]).item.systemName != item.systemName
		except AttributeError:
			logical = True
		if logical:
			return self.getItem(slotPos[0], slotPos[1]).set(item)
		else:
			cursorCount = item.count
			self.getItem(slotPos[0], slotPos[1]).item.count += cursorCount
			return None
	
	def getItem(self, x, y):
		return self.storage[y][x]
	
	def setItem(self, x, y, item):
		self.storage[y][x].set(item)
	
	def draw(self, surface):
		for i in range(self.height):
			for j in range(self.width):
				self.getItem(j, i).draw(j * 35, i * 35 + 62 + self.plusY, surface)

class Inventory:
	
	def __init__(self):
		self.cursor = None
		self.storageSection = StorageSection()
		self.accessPanel = AccessPanel()
		self.trashSlot = TrashSlot()
		
		self.accessPanel.putOn(WoodenAxe())
		self.accessPanel.putOn(WorkbenchItem())
		
		self.isWorkbenchOpened = False
		self.station = None
	
	def update(self, playerX, playerY, rad):
		if self.isWorkbenchOpened:
			if math.sqrt( (playerX - self.station.x) ** 2 + (playerY - self.station.y) ** 2 ) > rad:
				self.station.guiClose()
				self.isWorkbenchOpened = False
				self.station = None
			else:
				self.station.guiUpdate()
	
	def closeWorkbench(self):
		if self.isWorkbenchOpened:
			self.station.guiClose()
			self.isWorkbenchOpened = False
			self.station = None
	
	def openWorkbench(self, station):
		if not self.isWorkbenchOpened:
			self.station = station
			self.station.guiStart()
		else:
			self.station.guiClose()
			self.station = None
		self.isWorkbenchOpened = not self.isWorkbenchOpened
	
	def putOn(self, item):
		if self.storageSection.isFreeSlotFor(item):
			self.storageSection.putOn(item)
			return True
		elif self.accessPanel.isFreeSlotFor(item):
			self.accessPanel.putOn(item)
			return True
		else:
			return False
	
	def drop(self, mouseX, mouseY, x, y):
		if self.storageSection.mouseOn(mouseX, mouseY):
			slotPos = self.storageSection.getPosOnMouse(mouseX, mouseY)
			oDropped = self.storageSection.getItem(slotPos[0], slotPos[1]).getCopy()
			self.storageSection.setItem(slotPos[0], slotPos[1], None)
			if oDropped.item == None:
				return None
			return oDropped.item.getInDropped(x, y)
		elif self.accessPanel.mouseOn(mouseX, mouseY):
			slotX = self.accessPanel.getPosOnMouse(mouseX, mouseY)
			oDropped = self.accessPanel.getItem(slotX).getCopy()
			self.accessPanel.setItem(slotX, None)
			if oDropped.item == None:
				return None
			return oDropped.item.getInDropped(x, y)
	
	def mouseEvent(self, mouseX, mouseY, button):
		if button == 1:
			if self.storageSection.mouseOn(mouseX, mouseY):
				slotPos = self.storageSection.getPosOnMouse(mouseX, mouseY)
				self.cursor = self.storageSection.swap(self.cursor, slotPos)
			elif self.accessPanel.mouseOn(mouseX, mouseY):
				slotX = self.accessPanel.getPosOnMouse(mouseX, mouseY)
				self.cursor = self.accessPanel.swap(self.cursor, slotX)
			elif self.trashSlot.mouseOn(mouseX, mouseY):
				self.cursor = None
		elif button == 3:
			if self.storageSection.mouseOn(mouseX, mouseY):
				slotPos = self.storageSection.getPosOnMouse(mouseX, mouseY)
				try:
					if self.cursor != None:
						logical = self.storageSection.getItem(slotPos[0], slotPos[1]).item.systemName == self.cursor.systemName
					else:
						logical = not self.storageSection.getItem(slotPos[0], slotPos[1]).isEmpty()
				except AttributeError:
					logical = False
				if logical:
					if self.cursor != None:
						self.storageSection.getItem(slotPos[0], slotPos[1]).getOne()
						self.cursor.count += 1
					else:
						singleItem = self.storageSection.getItem(slotPos[0], slotPos[1]).getOne()
						self.cursor = singleItem
			elif self.accessPanel.mouseOn(mouseX, mouseY):
				slotX = self.accessPanel.getPosOnMouse(mouseX, mouseY)
				try:
					if self.cursor != None:
						logical = self.accessPanel.getItem(slotX).item.systemName == self.cursor.systemName
					else:
						logical = not self.accessPanel.getItem(slotX).isEmpty()
				except AttributeError:
					logical = False
				if logical:
					if self.cursor != None:
						self.accessPanel.getItem(slotX).getOne()
						self.cursor.count += 1
					else:
						singleItem = self.accessPanel.getItem(slotX).getOne()
						self.cursor = singleItem
		elif button == 4 or button == 5:
			if button == 4:
				self.accessPanel.wheel(1)
			else:
				self.accessPanel.wheel(-1)
	
	def draw(self, surface, mouseX, mouseY):
		self.storageSection.draw(surface)
		self.accessPanel.draw(surface)
		self.trashSlot.draw(surface)
		if self.cursor != None:
			surface.blit(self.cursor.getSprite(), [mouseX, mouseY])
		elif self.storageSection.mouseOn(mouseX, mouseY):
			slotPos = self.storageSection.getPosOnMouse(mouseX, mouseY)
			slot = self.storageSection.getItem(slotPos[0], slotPos[1])
			if slot.item != None:
				slot.item.drawTitles(mouseX, mouseY, surface)
		elif self.accessPanel.mouseOn(mouseX, mouseY):
			slotX = self.accessPanel.getPosOnMouse(mouseX, mouseY)
			slot = self.accessPanel.getItem(slotX)
			if slot.item != None:
				slot.item.drawTitles(mouseX, mouseY, surface)
		
		if self.isWorkbenchOpened:
			self.station.guiDraw(surface, mouseX, mouseY)
	
	def drawAccessPanel(self, surface):
		self.accessPanel.draw(surface)
		
		if self.isWorkbenchOpened:
			self.station.guiDraw(surface, pyg.mouse.get_pos()[0], pyg.mouse.get_pos()[1])

if __name__ != "__main__":
	DatabaseStatic.static_chest_storage = ChestStorage