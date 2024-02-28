import pygame as pyg
import json

class GameSounds:
	
	heartbeat = None
	
	@staticmethod
	def initializeGameSounds():
		GameSounds.heartbeat = pyg.mixer.Sound("rsrc\\sounds\\heartbeat.wav")

def playSound(sound, playCode = 0):
	jsonLoaded = open("settings.json", mode='r')
	data = json.load(jsonLoaded)
	jsonLoaded.close()
	if not data["soundOn"]:
		return
	
	volume = data["soundVolume"]
	
	del jsonLoaded
	del data
	
	sound.set_volume(volume)
	sound.play(playCode)

def stopSound(sound):
	sound.stop()

def playMusic(filename, playCode = -1):
	jsonLoaded = open("settings.json", mode='r')
	data = json.load(jsonLoaded)
	jsonLoaded.close()
	if not data["musicOn"]:
		stopMusic()
		return
	
	volume = data["musicVolume"]
	
	pyg.mixer.music.load("rsrc\\soundtracks\\" + filename + ".mp3")
	pyg.mixer.music.set_volume(volume)
	pyg.mixer.music.play(playCode)

def stopMusic():
	pyg.mixer.music.stop()

def localyze(text):
	jsonLoaded = open("settings.json", mode='r')
	data = json.load(jsonLoaded)
	jsonLoaded.close()
	
	lang = "local\\" + data["language"] + ".json"
	
	if lang == "local\\English.json":
		return text
	
	del data
	del jsonLoaded
	
	jsonLoaded = open(lang, mode='r')
	data = json.load(jsonLoaded)
	jsonLoaded.close()
	
	del jsonLoaded
	
	return data[text]