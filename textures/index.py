import sys, os
import pygame as pg

PLAYER_IMG = pg.image.load("textures/player/player.png")

TERRAIN = {
	"void" : pg.image.load("textures/void/void0000.png"),
	"grass" : pg.image.load("textures/terrain/grass.png"),
	"rock" : pg.image.load("textures/terrain/rock.png"),
	"mountain" : pg.image.load("textures/terrain/mountain.png")
}

ITEMS = {"heart" : pg.image.load("textures/items/heart.png"), "stone" : pg.image.load("textures/items/stone.png"), "empty" : pg.image.load("textures/items/empty_invisible.png")}

UI = 	{
	"pinv" : pg.image.load("textures/UI/Inventory/inventory.png"),
	"HUD" : {
			"hotbar" : pg.image.load("textures/UI/HUD/hotbar.png"),
			"hb_pointer" : pg.image.load("textures/UI/HUD/hb_pointer.png")
	}
}
