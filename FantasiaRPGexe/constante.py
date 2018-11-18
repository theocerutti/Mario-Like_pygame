#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygame
from fonctions import *
from pygame.locals import *

icon = pygame.image.load("lib/image/icon_rpg.png")


fenetreLargeur = 640
fenetreHauteur = 480

#COULEUR
BLANC = (255,255,255)
NOIR =  (  0, 0, 0)

#VARIABLE
afficheInvGui = False
degat = 0
clock = pygame.time.Clock()
coordSquelette = 0
vx, vy = 0, 0 #vecteurs vitesse
GRAVITE = 1.5 #gravité, plus est forte plus le perso ira vite vers le sol
vie = 194 #194 point de vie au départ (correspond a la taille de l'image de la barre de vie)

#FONT
pixel_font_dir = "lib/font/Fipps-Regular.otf"

#IMAGE,SURFACE LOAD
monde1 = load_img("lib/image/monde1.png") 					#taille 608x368
inventoryClose = load_img("lib/image/inventoryClose.png")	#taille 50x33
inventoryOpen = load_img("lib/image/inventoryOpen.png") #taille 50x41
inventory_gui = load_img("lib/image/inventory_gui.png") #taille 165x243
respawnButton = load_img("lib/image/respawn.png") #taille 187x72
pomme = load_img("lib/image/pomme.png")			#taille 38x38

listeSqueletteIMG = [
	load_img("lib/image/Skeleton Walk.png"),       #taille 286x33
	load_img("lib/image/Skeleton Walk Left.png"),  #taille
	load_img("lib/image/Skeleton Idle.png")]       #taille

listeBarreVieMana = [
	load_img("lib/image/barreVieManaSocle.png"),   #taille 113x29
	load_img("lib/image/barreVie.png"),            #taille 96x9
	load_img("lib/image/barreMana.png")]           #taille 80x4

#MUSIC,SON LOAD

son_pomme = load_sound("lib/sound/sfx_coin_double7.wav")
son_marche = load_sound("lib/sound/sfx_son_marche.wav")
