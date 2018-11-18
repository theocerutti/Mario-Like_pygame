#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygame
from fonctions import *
from pygame.locals import *

#icon = pygame.image.load("../lib/image/icon_rpg.png")

fenetreLargeur = 640
fenetreHauteur = 480

#COULEUR
BLANC = (255,255,255)
NOIR =  (  0, 0, 0)
VERT = (0, 255, 0)

#VARIABLE
info_ecran = pygame.display.Info() # infos de l'écran, taillex et y par ex
ecran_height = info_ecran.current_h
ecran_width = info_ecran.current_w

print("Ceci est votre résolution d'affichage",ecran_width,"x",ecran_height)

afficheInvGui = False
degat = 0
clock = pygame.time.Clock()
coordHero = 0
vx, vy = 0, 0 #vecteurs vitesse
GRAVITE = 1.5 #gravité, plus est forte plus le perso ira vite vers le sol

#FONT
pixel_font_dir = "lib/font/Fipps-Regular.otf"
pixel_font = pygame.font.Font(pixel_font_dir, 15)

#IMAGE,SURFACE LOAD

foreground = load_img("lib/image/foreground.png")
background1 = load_img("lib/image/background1.png")
background2 = load_img("lib/image/background2.png")
background3 = load_img("lib/image/background3.png")
background4 = load_img("lib/image/background4.png")

inventoryClose = load_img("lib/image/inventoryClose.png")	#taille 50x33
inventoryOpen = load_img("lib/image/inventoryOpen.png") #taille 50x41
inventory_gui = load_img("lib/image/inventory_gui.png") #taille 165x243
respawnButton = load_img("lib/image/respawn.png") #taille 187x72
pomme_img = load_img("lib/image/pomme.png")			#taille 38x38

heroLeft = load_img("lib/image/runHeroLeft.png")
heroRight = load_img("lib/image/runHeroRight.png")
heroIDLE = load_img("lib/image/idleHero.png")

barreVieSocle = load_img("lib/image/barreVieSocle.png")
barreVie = load_img("lib/image/barreVie.png")

img_ennemie = load_img("lib/image/Skeleton Walk Left.png")

img_trap = load_img("lib/image/piege.png")

fps_text = pixel_font.render("FPS:" + str(clock.get_fps()), True, NOIR)

#MUSIC,SON LOAD

son_kill_ennemie = load_sound("lib/sound/son_kill_ennemi.wav")
son_pomme = load_sound("lib/sound/sfx_coin_double7.wav")
son_marche = load_sound("lib/sound/sfx_son_marche.wav")


#TRANSFO IMAGE
foreground = transform_image(foreground, 3)
background1 = transform_image(background1, 3)
background2 = transform_image(background2, 3)
background3 = transform_image(background3, 3)
background4 = transform_image(background4, 3)

inventoryClose = transform_image(inventoryClose,1.5)
inventoryOpen = transform_image(inventoryOpen,1.5)
respawnButton = transform_image(respawnButton,0.5)

heroLeft = transform_image(heroLeft,2)
heroRight = transform_image(heroRight,2)
heroIDLE = transform_image(heroIDLE,2)

barreVieSocle = transform_image(barreVieSocle,2)
barreVie = transform_image(barreVie,2)

img_ennemie = transform_image(img_ennemie,2)

img_trap = transform_image(img_trap, 2)


#RECT
fps_rect = fps_text.get_rect(topleft = (10,440))
respawnButtonRect = respawnButton.get_rect(topleft = (500,400))
inventoryRect = inventoryOpen.get_rect(topleft = (fenetreLargeur - 100,20))
barreVieRect = barreVie.get_rect(topleft = (40,20))

foregroundRect = foreground.get_rect(topleft = (0,0))
background1Rect = background1.get_rect(topleft = (0,0))
background2Rect = background2.get_rect(topleft = (0,0))
background3Rect = background3.get_rect(topleft = (0,0))
background4Rect = background4.get_rect(topleft = (0,0))
