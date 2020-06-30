#!/usr/bin/python3.7
import sys

import pygame as pg
from settings import *
from textures import *

pg.init()

letters = {
pg.K_a : ['a', 'A'],
pg.K_b : ['b', 'B'],
pg.K_c : ['c', 'C'],
pg.K_d : ['d', 'D'],
pg.K_e : ['e', 'E'],
pg.K_f : ['f', 'F'],
pg.K_g : ['g', 'G'],
pg.K_h : ['h', 'H'],
pg.K_i : ['i', 'I'],
pg.K_j : ['j', 'J'],
pg.K_k : ['k', 'K'],
pg.K_l : ['l', 'L'],
pg.K_m : ['m', 'M'],
pg.K_n : ['n', 'N'],
pg.K_o : ['o', 'O'],
pg.K_p : ['p', 'P'],
pg.K_q : ['q', 'Q'],
pg.K_r : ['r', 'R'],
pg.K_s : ['s', 'S'],
pg.K_t : ['t', 'T'],
pg.K_u : ['u', 'U'],
pg.K_v : ['v', 'V'],
pg.K_w : ['w', 'W'],
pg.K_x : ['x', 'X'],
pg.K_y : ['y', 'Y'],
pg.K_z : ['z', 'Z'],
}

characters = {
pg.K_SPACE : ' ',
pg.K_0 : '0',
pg.K_1 : '1',
pg.K_2 : '2',
pg.K_3 : '3',
pg.K_4 : '4',
pg.K_5 : '5',
pg.K_6 : '6',
pg.K_7 : '7',
pg.K_8 : '8',
pg.K_9 : '9',
}

class Entry(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, size, func, font):
		self.game = game
		self.rect = pg.Rect((x, y), (w, size + 2))
		self.image = pg.Surface((w,size + 2))
		self.image.fill((255,255,255))
		self.cursor = pg.Surface((2,size)).convert_alpha()
		self.cursor.fill((128,128,128))
		self.cursor_rect = self.cursor.get_rect()
		self.cursor_rect.x = self.rect.x + 20
		self.cursor_rect.y = self.rect.y + 1
		self.c = 0
		self.cc = 1
		self.text = ''
		self.screen = game.screen
		self.func = func
		self.font = pg.font.Font(font, size)
		self.label = self.font.render(self.text, 1, (0,0,0))
		self.typing = false

	def add_char(self, char):
		if len(self.text) < MAX_WORLD_NAME_LENGTH:
			self.text += char
			self.label = self.font.render(self.text, 1, (0,0,0))

	def remove_char(self):
		self.text = self.text[:-1]
		self.label = self.font.render(self.text, 1, (0,0,0))

	def update(self):
		if self.c < 100 and self.cc == 1:
			self.c += self.cc
			self.cursor.fill((128,128,128))
		elif self.c > 0 and self.cc == -1:
			self.c += self.cc
			self.cursor.fill((0,0,0,0))
		else:
			self.cc *= -1

		keys = [pg.key.get_pressed()]
		for event in pg.event.get():
			if event.type == pg.QUIT:
				sys.exit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					sys.exit()
				if self.typing:
					if event.key in characters:
						self.add_char(characters[event.key])
					elif event.key in letters and keys:
						if keys[pg.KMOD_SHIFT]:
							self.add_char(letters[event.key[1]])
						else:
							self.add_char(letters[event.key][0])
					if event.key == pg.K_BACKSPACE:
						self.remove_char()
					if event.key == pg.K_RETURN:
						self.func()
			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1 and event.pos[1] > self.rect.y and event.pos[1] < self.rect.y + self.rect.height and event.pos[0] > self.rect.x and event.pos[0] < self.rect.x + self.rect.width:
					self.typing = true
				else:
					self.typing = false

		self.screen.blit(self.image, self.rect.topleft)
		if self.typing:
			self.screen.blit(self.cursor, self.cursor_rect.topleft)
		self.screen.blit(self.label, (self.rect.x + 2, self.rect.y + 1))
