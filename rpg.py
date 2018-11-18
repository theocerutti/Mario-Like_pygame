#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygame
from os import environ
from sys import exit
import time
from math import cos
from constantes import *
from fonctions import *

#Initialisation de pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

icon = pygame.image.load("lib/image/icon_rpg.png")
pygame.display.set_icon(icon) #initialisation de l'icône du jeu
environ['SDL_VIDEO_WINDOW_POS']="350,120" #on positionne la fenêtre

fenetre = pygame.display.set_mode((fenetreLargeur,fenetreHauteur))
pygame.display.set_caption("FantasiaRPG")

#MUSIC,SON LOAD
pygame.mixer.music.load("lib/music/Ludum Dare 38 - Track 9.wav") #on peut que initialisé UNE musique
pygame.mixer.music.play(-1,0.0) #-1 sert a répeter en boucle la musique
pygame.mixer.music.set_volume(0.35)
pygame.mixer.Sound.set_volume(son_marche,0.05)
pygame.mixer.Sound.set_volume(son_kill_ennemie,0.5)

#FONCTION/CLASSE

def shift_worldx(imgWorld, shift_x):
	"""Quand le joueur bouge à gauche/droite alors le monde se déplace"""
	imgWorld.x += shift_x

def shift_worldy(imgWorld, shift_y):
	"""Quand le joueur bouge en bas/haut alors le monde se déplace"""
	imgWorld.y += shift_y

class Player():
	"""Classe permettant de gérer le joueur"""

	def __init__(self, image, longueurSpriteSheetX, grandeurImgX, posX, posY):
		"""Constructeur de la classe"""

		self.image = image
		self.rect = self.image.get_rect(topleft = (posX,posY))
		self.gravite = 1.5
		self.vx = 0
		self.vy = 0
		self.grandeurImgX = grandeurImgX
		self.coord_spritesheet = 0
		self.longueurSpriteSheetX = longueurSpriteSheetX
		self.rect = self.rect.inflate(-self.longueurSpriteSheetX + self.grandeurImgX, 0) #je rétrécit le rect à la taille de l'image de la spritesheet
		self.last_run = 0
		self.period_anim = 0.05
		self.degat = 0
		self.vie = 200 #200 point de vie au départ (correspond a la taille de l'image de la barre de vie)

	def anim(self):
		"""Fonction permettant de faire l'animation du personnage. De plus, on peut modifier la vitesse d'animation en diminuant self.periode_anim"""

		if time.time() - self.last_run > self.period_anim:
			self.coord_spritesheet += self.grandeurImgX
			#l'animation
			if self.coord_spritesheet > self.longueurSpriteSheetX - self.grandeurImgX:
				self.coord_spritesheet = 0
			self.last_run = time.time()

	def move(self, vitesseX):
		"""Fonction permettant le mouvement du personnage"""
		self.vx = (pressed[K_RIGHT] - pressed[K_LEFT]) * vitesseX

	def calcul_grav(self):
		"""Fonction permettant de calculer la gravité exercée sur le personnage"""

		self.vy += self.gravite #gravité diminuant constamment la posY du perso
		self.vy = min(20, self.vy) #permet de limiter vy à 20, pour pas que l'on tombe de + en + vite à l'infini
		self.rect.y += self.vy #on ajoute vy au rect y
		self.rect.x += self.vx #on ajoute vx au rect x

	def look_if_dead(self):
		"""Fonction permettant la gestion de la mort, des degats, et du respawn"""

		#degat/vie
		if self.degat > 0:
			self.vie -= self.degat #on update la vie on soustrait les degats à la vie (la vie est la position du rectX de la vie donc si on baisse la vie on bouge vers la gauche la vie)
			self.degat = 0 #on remet les degats à 0 sinon à chaque tour de boucle les dégâts se remettront tout le temps

		#quand on a plus de vie
		if self.vie < 0:
			print("Vous êtes mort, le programme s'arrête")
			exit(0)

	def respawn(self, degat, posX, posY):
		"""Fonction permettant le respawn du hero. On peut lui ajouter des degats à chaque respawn"""

		self.degat = 50
		self.rect.x = foregroundRect.x + posX
		self.rect.y = foregroundRect.y + posY
		background4Rect.x, background4Rect.y = foregroundRect.x, foregroundRect.y
		background3Rect.x, background3Rect.y = foregroundRect.x, foregroundRect.y
		background2Rect.x, background2Rect.y = foregroundRect.x, foregroundRect.y
		background1Rect.x, background1Rect.y = foregroundRect.x, foregroundRect.y

	def update(self):
		"""Fonction permettant l'update du personnage"""

		self.look_if_dead()
		self.calcul_grav() #on calcule la gravité avant d'update
		fenetre.blit(self.image,self.rect,(self.coord_spritesheet,0,self.grandeurImgX,70))

class Enemy():
	"""Classe permettant la gestion des ennemis"""

	def __init__(self, image, longueurSpriteSheetX, grandeurImg_ennemiX, posX, posY):
		"""Constructeur de la classe Enemy"""

		self.image = image
		self.image = pygame.transform.flip(self.image, True, False) #on fait le miroir vertical de l'image et pas horizontal
		self.rect = self.image.get_rect(topleft = (posX,posY))
		self.posX = posX

		#distanceTravel
		self.distanceXtravel = 0
		self.distanceYtravel = 0

		#pour l'anim
		self.longueurSpriteSheetX = longueurSpriteSheetX
		self.grandeurImgX = grandeurImg_ennemiX
		self.rect = self.rect.inflate(-self.longueurSpriteSheetX + self.grandeurImgX,0) #je rétrécit le rect à la taille de l'image de la spritesheet
		self.coord_spritesheet = 0
		self.last_run = 0
		self.period_anim= 0.04

	def kill(self):
		"""Destructeur de la classe, permet alors de "suprimmer" l'ennemi en le mettant hors de l'écran !"""

		print("Destruction de l'objet: ", self)
		self.posX = -10000 #on le téleporte à un endroit que l'on ne peut pas voir, je ne le suprimme PAS

	def distanceTravel(self, vitesse, distanceTravel):
		"""Fonction permettant la gestion du travel de l'ennemi:
				-distanceTravel : distance aller/retour que l'ennemi va faire (quand il va "rôder")
				A INTEGRER DANS LA BOUCLE EVENEMENTIELLE"""

		self.distanceXtravel += vitesse

		self.rect.x = (cos(self.distanceXtravel) * distanceTravel) + self.posX

		if cos(self.distanceXtravel) >= 0.999: #chaque fois que le perso va tout à droite (cos(x) = 1) ou à gauche (cos(x) = -1) l'image de l'ennemi est flip horizontalement
			self.image = pygame.transform.flip(self.image, True, False)
		elif cos(self.distanceXtravel) <= -0.999:
			self.image = pygame.transform.flip(self.image, True, False)

	def update(self):
		"""Fonction permettant d'update l'ennemi"""

		self.anim()
		fenetre.blit(self.image,self.rect,(self.coord_spritesheet,0,self.grandeurImgX,66))

	def anim(self):
		"""Fonction permettant de faire l'animation de l'ennemi. De plus, on peut modifier la vitesse d'animation en diminuant self.periode_anim"""

		if time.time() - self.last_run > self.period_anim:
			self.coord_spritesheet += self.grandeurImgX
			#l'animation
			if self.coord_spritesheet > self.longueurSpriteSheetX - self.grandeurImgX:
				self.coord_spritesheet = 0
			self.last_run = time.time()

class Trap():
	"""Classe permettant la création de pièges"""

	def __init__(self, image, posX, posY):
		"""Constructeur de la classe"""

		self.image = image
		self.rect = self.image.get_rect(topleft = (posX, posY))

	def update(self):
		"""Fonction permettant l'update des traps"""
		fenetre.blit(self.image, self.rect)

class Plateforme():
	"""Classe permettant la construction des plateformes du niveau"""

	def __init__(self):
		"""Constructeur des plateformes"""

		largeur,hauteur = 1,1 #on met de base 1 car après on le change dans le constructeur de Level

		self.image = pygame.Surface([largeur, hauteur])
		self.image.fill(NOIR)

		self.rect = self.image.get_rect()
		self.plateforme_list_rect = []
		self.plateforme_list_image = []

		#pour le dynamicMove des murs
		self.drag = False
		self.rect_indice = -1
		self.offsetx = 0
		self.offsety = 0

	def ConstructLevel(self):
		"""Fonction permettant la construction des plateformes dans le level"""

		# largeur,hauteur,posX,posY

		self.level = [[331, 800, 0, 296],#0
				 [271, 50, 488, 392],  #1
				 [225, 800, 583, 680], #2
				 [48, 800, 804, 727],  #3
				 [171, 800, 852, 821], #4
				 [295, 800, 1018, 777],#5
				 [245, 800, 1306, 727],#6
				 [155, 800, 1547, 681],#7
				 [1090, 800, 1685, 584],#8
				 [265, 50, 2940, 390],  #9
				 [238, 500, 3019, 680], #10
				 [65, 500, 3242, 820],  #11
				 [50, 500, 3415, 820],  #12
				 [120, 500, 3300, 915], #13
				 [120, 50, 3325, 490],  #14
				 [270, 500, 3465, 780], #15
				 [70, 100, 3515, 585],  #16
				 [60, 55, 3583, 630],	#17
				 [50, 21, 3635, 674],	#18
				 [100, 500, 3947, 780],	#19
				 [100, 500, 3993, 731],	#20
				 [230, 500, 4043, 681],	#21
				 [30,300,-30,0], #mur limite gauche   #22
				 [30,1000,4266,0] #mur limite droite  #23
				 ]

		#on va créer 2 listes où il y a d'une part les images et d'autre part les rects des murs du level
		for plateforme in range(len(self.level)):
			self.image = pygame.Surface((self.level[plateforme][0], self.level[plateforme][1]))
			self.rect = self.image.get_rect(topleft = (self.level[plateforme][2],self.level[plateforme][3]))

			self.plateforme_list_image.append(self.image)
			self.plateforme_list_rect.append(self.rect)

	def dynamicMove(self, liste, monderectx, monderecty):
		"""Cette fonction permet le déplacement dynamique des murs. DANS le jeu, on va pouvoir bouger, et connaître ses coordonnées"""

		if event.type == MOUSEBUTTONDOWN: #lorsque que je clique gauche sur un des murs alors la valeur drag vaut True on peut alors le bouger. On calcul aussi le offset. En effet, si on ne fait pas le calcul alors le mur sera toujours pris en haut à gauche et on pourra difficilement le bouger !
			if event.button == 1:
				for i in range(len(liste)):
					if liste[i].collidepoint(event.pos):
						self.rect_indice = i
						self.drag = True
						self.offsetx = liste[i].x - event.pos[0]
						self.offsety = liste[i].y - event.pos[1]


		elif event.type == MOUSEBUTTONUP: #si on relâche le bouton alors la valeur drag se met à False, on peut plus bouger le mur
			if event.button == 1:
				self.drag = False

		elif event.type == MOUSEMOTION: #si drag vaut True, on peut le bouger, le mur va suivre la souris que lorsque le bouton gauche de la souris sera enfoncé
			if self.drag:
				liste[self.rect_indice].x = event.pos[0] + self.offsetx
				liste[self.rect_indice].y = event.pos[1] + self.offsety

		#on affiche les coordonnées du mur sélectionné que lorsque qu'un mur a été déplacé (normal)
		if self.rect_indice != -1: #lorsque rect_indice vaut de base -1 cela veut dire qu'on n'a pas encore bougé de murs
			print("\nMur n°", self.rect_indice)
			print("coord x: ",liste[self.rect_indice].x - monderectx,"\ncoord y: ", liste[self.rect_indice].y - monderecty)

	def update(self):
		"""Fonction permettant l'update des murs, il est utile et utilisable que lorsque l'on est en devmode"""

		for mur in range(len(self.plateforme_list_rect)):
			fenetre.blit(self.plateforme_list_image[mur],self.plateforme_list_rect[mur])

class Item():
	"""Classe permettant la création d'item :
	-item droppable
	-item à récuperer (ex : étoiles,pommes)
	-le mouvement dynamique à la souris de l'objet
	-etc
	"""
	def __init__(self,img,score = 0):
		"""Constructeur de l'objet item"""

		self.image = img
		self.score = score
		self.rect = self.image.get_rect()

		#pour le dynamicMove des items
		self.drag = False
		self.rect_indice = -1
		self.offsetx = 0
		self.offsety = 0

	def ConstructItem(self):
		"""Fonction permettant de placer les items dans le level"""

		# posX, posY
		level_pomme = [[50, 230], #0
				 	[550, 330],  #1
				 	[603, 616],	 #2
				 	[816, 675],  #3
				 	[917, 700 ],	 #4
				 	[1150, 720], #5
				 	[1415, 670], #6
					[2277, 456], #7
					[2367, 396], #8
					[2454, 456], #9
					[2913, 525], #10
					[3048, 185], #11
					[3343, 716], #12
					[3768, 460], #13
					[3778, 643], #14
					[3796, 626], #15
					[3823, 624], #16
					[3848, 629], #17
					[3868, 645], #18
					]

		self.pomme_liste = [] #on créer une liste contenant le rect des pommes
		for pomme in range(len(level_pomme)):
			self.rect = self.image.get_rect(topleft = (level_pomme[pomme][0],level_pomme[pomme][1]))
			self.pomme_liste.append(self.rect)

	def dynamicMove(self, liste, monderectx, monderecty):
		"""Cette fonction permet le déplacement dynamique des items. DANS le jeu, on va pouvoir bouger, et connaître ses coordonnées"""

		if event.type == MOUSEBUTTONDOWN: #lorsque que je clique gauche sur un des items alors la valeur drag vaut True on peut alors le bouger. On calcul aussi le offset. En effet, si on ne fait pas le calcul alors le mur sera toujours pris en haut à gauche et on pourra difficilement le bouger !
			if event.button == 1:
				for i in range(len(liste)):
					if liste[i].collidepoint(event.pos):
						self.rect_indice = i
						self.drag = True
						self.offsetx = liste[i].x - event.pos[0]
						self.offsety = liste[i].y - event.pos[1]


		elif event.type == MOUSEBUTTONUP: #si on relâche le bouton alors la valeur drag se met à False, on peut plus bouger l'item
			if event.button == 1:
				self.drag = False

		elif event.type == MOUSEMOTION: #si drag vaut True, on peut le bouger, le mur va suivre la souris que lorsque le bouton gauche de la souris sera enfoncé
			if self.drag:
				liste[self.rect_indice].x = event.pos[0] + self.offsetx
				liste[self.rect_indice].y = event.pos[1] + self.offsety

		#on affiche les coordonnées de l'item sélectionné que lorsque qu'un item a été déplacé (normal)
		if self.rect_indice != -1: #lorsque rect_indice vaut de base -1 cela veut dire qu'on n'a pas encore bougé d'items
			print("\nItem n°", self.rect_indice)
			print("coord x: ",liste[self.rect_indice].x - monderectx,"\ncoord y: ", liste[self.rect_indice].y - monderecty)

	def update(self):
		"""Permet la gestion des items recoltables!"""

		for pomme in range(len(self.pomme_liste)):
			if hero.rect.colliderect(self.pomme_liste[pomme]):
				self.pomme_liste[pomme].x += 1000 #c'est pour sortir l'image hors de l'écran et le faire disparaitre
				self.pomme_liste[pomme].y += 1000
				self.score += 10
				hero.vie += 10
				son_pomme.play()
			fenetre.blit(self.image,self.pomme_liste[pomme])

class Compteur():
	def __init__(self):
		"""Constructeur de la classe compteur"""

		self.pixel_font = pygame.font.Font(pixel_font_dir, 15)
		self.image = pygame.Surface((100,50))
		self.rect = self.image.get_rect()
		self.text_surf = self.pixel_font.render(str(pomme.score) + "pts", True, (10, 10, 10))

	def update(self):
		"""Fonction permettant l'update du compteur et affiche un message lorsque que tout les items ont été pris"""

		if pomme.score < len(pomme.pomme_liste) * 10:
			self.text_surf = self.pixel_font.render(str(pomme.score) + "pts", True, (10, 10, 10))
			fenetre.blit(self.text_surf,(250,15))
		else:
			self.pixel_font = pygame.font.Font(pixel_font_dir, 25)
			self.text_surf = self.pixel_font.render("Vous avez gagné !!", True, (10, 10, 10))
			fenetre.blit(self.text_surf,(155,200))

class Level():
	"""Permet de créer le niveau, le dessiner, et l'update"""

	def __init__(self):
		"""Constructeur de la classe Level"""

		self.limite_droite = 1424*3 #largeur du monde x
		self.limite_gauche = 0

	def shift_world(self):
		"""Fonction permettant le shift du level"""

		#le shift du level doit se faire que si le héro n'a pas atteint la limite gauche ou droite
		if self.limite_droite >  (hero.rect.x + (fenetreLargeur - 300)) - foregroundRect.x and self.limite_gauche < hero.rect.x - 199 - foregroundRect.x:
			#explication : du calcul de la limite de droite :
			# -> foregroundRect.x car lorsque il y a le shift alors le x prend valeur negatif donc on fait l'inverse
			# après on fait la pos initiale du perso + toute la largeur de la fenetre jusqu'au shift droit puis on soustraie le x foregroundRect
			#on ne fait pas la même pour la gauche car il n'y a aucun effet de shift

			#droite
			if hero.rect.x > 300:
				diff = hero.rect.x - 300
				hero.rect.x = 300
				shift_worldx(foregroundRect, -diff)
				shift_worldx(background1Rect, -diff + 2) #1 = champi+plaine, je dois avoir -6 (-8 + 2 sachant que diff = 8)
				shift_worldx(background2Rect, -diff + 3) #2 = back plaine
				shift_worldx(background3Rect, -diff + 4) #3 nuage
				shift_worldx(background4Rect, -diff + 5) #4 ciel
				for ennemi in range(len(ennemi_list)):#on ne peut pas faire shift_worldx(squelette_ennemie.rect,-diff) car ca écrase la variable après
					ennemi_list[ennemi].posX += -diff
				for trap in range(len(trap_list)):
					shift_worldx(trap_list[trap].rect, -diff)
				for i in range(len(mur.level)):
					shift_worldx(mur.plateforme_list_rect[i], -diff)
				for i in range(len(pomme.pomme_liste)):
					shift_worldx(pomme.pomme_liste[i], -diff)

		    #à gauche
			if hero.rect.x < 199:
				diff = 199 - hero.rect.x
				hero.rect.x = 199
				shift_worldx(foregroundRect, diff)
				shift_worldx(background1Rect, diff - 2) #je dois avoir 6
				shift_worldx(background2Rect, diff - 3)
				shift_worldx(background3Rect, diff - 4)
				shift_worldx(background4Rect, diff - 5)
				for ennemi in range(len(ennemi_list)):
					ennemi_list[ennemi].posX += diff
				for trap in range(len(trap_list)):
					shift_worldx(trap_list[trap].rect, diff)
				for i in range(len(mur.level)):
					shift_worldx(mur.plateforme_list_rect[i], diff)
				for i in range(len(pomme.pomme_liste)):
					shift_worldx(pomme.pomme_liste[i], diff)

			#EN HAUT
			if hero.rect.y < 150:
				diff = 150 - hero.rect.y
				hero.rect.y = 150
				shift_worldy(foregroundRect, diff)
				shift_worldy(background1Rect, diff)
				shift_worldy(background2Rect, diff)
				shift_worldy(background3Rect, diff)
				shift_worldy(background4Rect, diff)
				for ennemi in range(len(ennemi_list)):
					shift_worldy(ennemi_list[ennemi].rect, diff)
				for trap in range(len(trap_list)):
					shift_worldy(trap_list[trap].rect, diff)
				for i in range(len(mur.level)):
					shift_worldy(mur.plateforme_list_rect[i], diff)
				for i in range(len(pomme.pomme_liste)):
					shift_worldy(pomme.pomme_liste[i], diff)

			#en bas
			if hero.rect.y > 200:
				diff = 200 - hero.rect.y
				hero.rect.y = 200
				shift_worldy(foregroundRect, diff)
				shift_worldy(background1Rect, diff)
				shift_worldy(background2Rect, diff)
				shift_worldy(background3Rect, diff)
				shift_worldy(background4Rect, diff)
				for ennemi in range(len(ennemi_list)):
					shift_worldy(ennemi_list[ennemi].rect, diff)
				for trap in range(len(trap_list)):
					shift_worldy(trap_list[trap].rect, diff)
				for i in range(len(mur.level)):
					shift_worldy(mur.plateforme_list_rect[i], diff)
				for i in range(len(pomme.pomme_liste)):
					shift_worldy(pomme.pomme_liste[i], diff)

	def affichage(self):
		"""Fonction permettant d'afficher toutes les images"""

		fenetre.blit(background4, background4Rect)
		fenetre.blit(background3, background3Rect)
		fenetre.blit(background2, background2Rect)
		fenetre.blit(background1, background1Rect)
		fenetre.blit(foreground, foregroundRect)
		for trap in range(len(trap_list)):
			trap_list[trap].update()
		for ennemi in range(len(ennemi_list)):
			ennemi_list[ennemi].update()
		hero.update()
		#mur.update() #on blite pour voir les murs (devmode)
		fenetre.blit(barreVieSocle, (10,10))
		fenetre.blit(barreVie,barreVieRect, (0,0,hero.vie,18)) #la variable vie correspond à l'endroit ou la barreVie est blit, à 200pts de vies, la barre est totalement blit
		fenetre.blit(inventoryBase,inventoryRect)
		fenetre.blit(respawnButton,respawnButtonRect)
		pomme.update()
		compteurScore.update()
		fenetre.blit(fps_text, fps_rect)
		if afficheInvGui == True: #si on clique sur la sacoche, ca blit le gui inv
			fenetre.blit(inventory_gui,(240,120))

#AUTRE
pygame.key.set_repeat(1, 30)
pygame.time.set_timer(USEREVENT, 1000)
inventoryBase = inventoryClose #pour que l'image de base soit l'inventaire qui est fermé
mur = Plateforme()
level = Level()
pomme = Item(pomme_img)
pomme.ConstructItem()
compteurScore = Compteur()
squelette_ennemie = Enemy(img_ennemie, 572, 44, 600, 325)
squelette_ennemie2 = Enemy(img_ennemie, 572, 44, 1130,710)
squelette_ennemie3 = Enemy(img_ennemie, 572, 44, 2300,515)
squelette_ennemie4 = Enemy(img_ennemie, 572, 44, 2300, 515)
squelette_ennemie5 = Enemy(img_ennemie, 572, 44, 3120, 620)
ennemi_list = []
ennemi_list.append(squelette_ennemie)
ennemi_list.append(squelette_ennemie2)
ennemi_list.append(squelette_ennemie3)
ennemi_list.append(squelette_ennemie4)
ennemi_list.append(squelette_ennemie5)
trap1 = Trap(img_trap, 900,770)
trap2 = Trap(img_trap, 3322, 860)
trap3 = Trap(img_trap, 3348, 427)
trap_list = []
trap_list.append(trap1)
trap_list.append(trap2)
trap_list.append(trap3)
hero = Player(heroRight,386, 48, 0, 200)
mur.ConstructLevel() #on construit et on place les murs


#Boucle événementielle
continuer = True
while continuer:

	for event in [pygame.event.poll()]:
		if event.type == QUIT: #si je clique sur la croix, le jeu se ferme
			continuer = False

		elif event.type == KEYDOWN:
			if event.key == K_SPACE and (hero.vy == 0 or hero.vy == hero.gravite): #permet de faire un saut que lorsque le perso est au sol (soit quand vy=0 ou vy == gravite)
				hero.vy = -20 #hauteur du saut
				hero.gravite = 1.5
				hero.update() #on doit faire l'update ici sinon on ne voit pas l'anim de saut!

		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1 and inventoryRect.collidepoint(event.pos) and afficheInvGui == True: #pour fermer l'inventaire
				inventoryBase = inventoryClose
				afficheInvGui = False

			elif event.button == 1 and inventoryRect.collidepoint(event.pos): #pour ouvrir l'inventaire grâce à la souris
				inventoryBase = inventoryOpen
				afficheInvGui = True

			elif event.button and respawnButtonRect.collidepoint(event.pos): #lorsque l'on clique sur le bouton respawn cela nous ramène au début
				hero.respawn(50, 200, 200)

			elif event.button == 1:
				x_mouse, y_mouse = pygame.mouse.get_pos()
				print("Coordonnées x:",x_mouse - foregroundRect.x,"; y:", y_mouse - foregroundRect.y)

		if event.type == USEREVENT:
			fps_text = pixel_font.render("FPS:" + str(round(clock.get_fps(),2)), True, NOIR)

		pomme.dynamicMove(pomme.pomme_liste, foregroundRect.x, foregroundRect.y)
		#mur.dynamicMove(mur.plateforme_list_rect, foregroundRect.x, foregroundRect.y) #devmode-- c'est pour bouger les murs

	#mouvement/animation du hero
	pressed = pygame.key.get_pressed()
	if pressed[K_RIGHT]:
		hero.image = heroRight
		hero.longueurSpriteSheetX = 384
		hero.anim()
		hero.move(8)
		if hero.vy == 0 or hero.vy == 1.5: #si je suis sur une plateforme
			son_marche.play() #on active le son de marche
	elif pressed[K_LEFT]:
		hero.image = heroLeft
		hero.longueurSpriteSheetX = 384
		hero.anim()
		hero.move(8)
		if hero.vy == 0 or hero.vy == 1.5:
			son_marche.play()
	else:
		hero.image = heroIDLE
		hero.longueurSpriteSheetX = 576
		hero.anim()
		hero.move(0)


	#-------------------Logique de jeu--------------------------

	#lorsque le perso va en trop bas (en gros qu'il tombe dans le trou) alors il se fait respawn (il est mort)
	if foregroundRect.y < -825:
		hero.respawn(50, 200, 200)
		print("Vous êtes mort en tombant, vous respawnez, vous avez perdu 50 pts de vies !")

	#colision
	for i in range(len(mur.level)):
		if mur.plateforme_list_rect[i].collidepoint(hero.rect.midtop):
			hero.rect.top = mur.plateforme_list_rect[i].bottom
		if mur.plateforme_list_rect[i].collidepoint(hero.rect.midbottom):
			hero.rect.bottom = mur.plateforme_list_rect[i].top
			hero.gravite = 0 #on met la gravité à 0 lorsque l'on est sur une plateforme
			hero.vy = 0 #on met vy à 0 lorsque l'on est sur une plateforme
		else:
			hero.gravite = 1.5 #si on n'est pas sur une plateforme on remet la gravité

		if mur.plateforme_list_rect[i].collidepoint(hero.rect.midleft):
			hero.rect.left = mur.plateforme_list_rect[i].right
		if mur.plateforme_list_rect[i].collidepoint(hero.rect.midright):
			hero.rect.right = mur.plateforme_list_rect[i].left

	#collision de l'ennemi
	for ennemi in range(len(ennemi_list)):
		if ennemi_list[ennemi].rect.collidepoint(hero.rect.midbottom): #si on touche la partie haute d'un ennemie alors on le kill:
			son_kill_ennemie.play()
			hero.vy = 0
			hero.vy -= 10 #pour faire une sorte de rebond
			ennemi_list[ennemi].kill()
		elif ennemi_list[ennemi].rect.colliderect(hero.rect):
			hero.degat = 10

	#collision des traps
	for trap in range(len(trap_list)):
		if trap_list[trap].rect.colliderect(hero.rect): #si on touche un piege
			hero.degat = 10

	#calcul position ennemie
	squelette_ennemie.distanceTravel(0.03, 100)
	squelette_ennemie2.distanceTravel(0.03, 120)
	squelette_ennemie3.distanceTravel(0.02, 200)
	squelette_ennemie4.distanceTravel(0.03, 200)
	squelette_ennemie5.distanceTravel(0.03, 80)

	#Shift_world:
	level.shift_world()

	#L'affichage du jeu
	level.affichage()

	#Rafraichissement
	pygame.display.flip()
	clock.tick(30)

