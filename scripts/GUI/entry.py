#!/usr/bin/python3.7
import sys

import pygame as pg
from settings import *
from textures import *

pg.init()

characters = {
pg.K_a : 'a',
pg.K_b : 'b',
pg.K_c : 'c',
pg.K_d : 'd',
pg.K_e : 'e',
pg.K_f : 'f',
pg.K_g : 'g',
pg.K_h : 'h',
pg.K_i : 'i',
pg.K_j : 'j',
pg.K_k : 'k',
pg.K_l : 'l',
pg.K_m : 'm',
pg.K_n : 'n',
pg.K_o : 'o',
pg.K_p : 'p',
pg.K_q : 'q',
pg.K_r : 'r',
pg.K_s : 's',
pg.K_t : 't',
pg.K_u : 'u',
pg.K_v : 'v',
pg.K_w : 'w',
pg.K_x : 'x',
pg.K_y : 'y',
pg.K_z : 'z',
pg.K_SPACE : ' '
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


		for event in pg.event.get():
			if event.type == pg.QUIT:
				sys.exit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					sys.exit()
				if self.typing:
					if event.key in characters:
						self.add_char(characters[event.key])
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


# class Screen():
# 	def __init__(self):
# 		self.screen = pg.display.set_mode((400, 300))
# 		self.entry = Entry(self, 10, 10, 100, 20, self.dick)
#
# 	def dick(self):
# 		print('You have typed: ', self.entry.text)
#
# 	def update(self):
# 		self.entry.update()
# 		if self.entry.c == 500:
# 			print(self.entry.text)
# 		pg.display.update()
#
#
#
# s = Screen()
# while True:
# 	s.update()
