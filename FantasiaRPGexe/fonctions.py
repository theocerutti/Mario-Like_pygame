#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

def load_img(name):
	"""Load une image et la retourne"""
	try:
		image = pygame.image.load(name)
		if image.get_alpha() is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except pygame.error:
		print("ERROR -- L'image : ", name , " ne peut être afficher dans le module fonction car pygame.display n'est pas initialisé.")
	return image

def load_sound(name):
	"""Load une son et la retourne"""
	try:
		son = pygame.mixer.Sound(name)
	except pygame.error:
		print("ERROR -- Le son : ", name , " ne peut être initialisé")
	return son

def transform_image(image,taille_x,taille_y):
	"""Transforme une image selon la taille mise en argument"""
	image = pygame.image.transform(image,taille_x,taille_y)
	return image

