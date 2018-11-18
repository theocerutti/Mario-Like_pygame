#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()


def load_img(name):
	"""Load une image et la retourne-
		   Arguments :
	   		- name : path de l'image"""
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
	"""Load une son et la retourne-
	   Arguments :
	   		- name : path du son"""
	try:
		son = pygame.mixer.Sound(name)
	except pygame.error:
		print("ERROR -- Le son : ", name , " ne peut être initialisé")
	return son


def transform_image(image, multiplicateur):
	"""Transforme une image selon la taille mise en argument-
	   Arguments :
	   		- image : objet de type Surface attendu
	   		- multiplicateur : permet de multiplier la taille de l'image, int ou float sont acceptés"""
	try:
		imageX , imageY = image.get_size()
		image = pygame.transform.scale(image,(int(imageX*multiplicateur),int(imageY*multiplicateur)))
	except pygame.error:
		print("ERROR -- L'image :", image, " ne peut être initialisé")
	return image
