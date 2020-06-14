import sys, os
import pygame as pg

PLAYER_IMG = pg.image.load("textures/player/player.png")

VOID = [pg.image.load("textures/void/void0000.png"),
		pg.image.load("textures/void/void0001.png"),
		pg.image.load("textures/void/void0002.png"),
		pg.image.load("textures/void/void0003.png")
		]

TERRAIN = {'grass' : pg.image.load("textures/terrain/grass.png"), 'rock' : pg.image.load("textures/terrain/rock.png"), 'mountain' : pg.image.load("textures/terrain/mountain.png")}

ITEMS = {'heart' : pg.image.load("textures/items/heart.png"), 'stone' : pg.image.load("textures/items/stone.png")}
