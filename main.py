# moduli
import pygame, sys
import numpy as np

# inicijalizacija igre
pygame.init()



# boje

pozadina = (255,255,255)
BOJA_LINIJE = (0, 0, 0)
BOJA_KRUGA = (0,0,0)
BOJA_IKSA = (0,0,0)


# konstante

SIRINA = 600
VISINA = 600
DEBLJINA_LINIJE = 15
CRTA = 15
VELICINA_POLJA = 200
PROMJER_KRUGA = 60
SIRINA_KRUGA = 15
SIRINA_IKSA = 25
RAZMAK = 55
# ------
# graficki prikaz
# ------
displej = pygame.display.set_mode( (SIRINA, VISINA) )
pygame.display.set_caption( 'Iks Oks' )
displej.fill( pozadina )

# -------------
# logicka ploca
# -------------
ploca = np.zeros( (3, 3) )

# ---------
# funkcije
# ---------
def crtaj_linije():
	# 1 horizontal
	pygame.draw.line( displej, BOJA_LINIJE, (30, VELICINA_POLJA), (SIRINA-30, VELICINA_POLJA),CRTA)
	# 2 horizontal
	pygame.draw.line( displej, BOJA_LINIJE, (30, 2 * VELICINA_POLJA), (SIRINA-30, 2 * VELICINA_POLJA),CRTA)

	# 1 vertical
	pygame.draw.line( displej, BOJA_LINIJE, (VELICINA_POLJA, 30), (VELICINA_POLJA, VISINA-30),CRTA)
	# 2 vertical
	pygame.draw.line( displej, BOJA_LINIJE, (2 * VELICINA_POLJA, 30), (2 * VELICINA_POLJA, VISINA-30),DEBLJINA_LINIJE )

def crtaj_figure():
	for row in range(3):
		for col in range(3):
			if ploca[row][col] == 1:
				pygame.draw.circle( displej, BOJA_KRUGA, (int( col * VELICINA_POLJA + VELICINA_POLJA//2 ), int( row * VELICINA_POLJA + VELICINA_POLJA//2 )), PROMJER_KRUGA, SIRINA_KRUGA )
			elif ploca[row][col] == 2:
				pygame.draw.line( displej, BOJA_IKSA, (col * VELICINA_POLJA + RAZMAK, row * VELICINA_POLJA + VELICINA_POLJA - RAZMAK), (col * VELICINA_POLJA + VELICINA_POLJA - RAZMAK, row * VELICINA_POLJA + RAZMAK), SIRINA_IKSA)
				pygame.draw.line( displej, BOJA_IKSA, (col * VELICINA_POLJA + RAZMAK, row * VELICINA_POLJA + RAZMAK), (col * VELICINA_POLJA + VELICINA_POLJA - RAZMAK, row * VELICINA_POLJA + VELICINA_POLJA - RAZMAK), SIRINA_IKSA )

def oznaci_polje(row, col, igrac):
	ploca[row][col] = igrac

def dostupno_polje(row, col):
	return ploca[row][col] == 0

def puna_ploca():
	for row in range(3):
		for col in range(3):
			if ploca[row][col] == 0:
				return False

	return True

def pobjeda(igrac):
	# vertical win check
	for col in range(3):
		if ploca[0][col] == igrac and ploca[1][col] == igrac and ploca[2][col] == igrac:
			crtaj_vertikalnu_dobitnu_liniju(col, igrac)
			return True

	# horizontal win check
	for row in range(3):
		if ploca[row][0] == igrac and ploca[row][1] == igrac and ploca[row][2] == igrac:
			crtaj_horizontalnu_dobitnu_liniju(row, igrac)
			return True

	# asc diagonal win check
	if ploca[2][0] == igrac and ploca[1][1] == igrac and ploca[0][2] == igrac:
		crtaj_kosu_dobitnu_liniju(igrac)
		return True

	# desc diagonal win chek
	if ploca[0][0] == igrac and ploca[1][1] == igrac and ploca[2][2] == igrac:
		crtaj_obrnutu_kosu_dobitnu_liniju(igrac)
		return True

	return False

def crtaj_vertikalnu_dobitnu_liniju(col, igrac):
	posX = col * VELICINA_POLJA + VELICINA_POLJA//2

	if igrac == 1:
		boja = BOJA_KRUGA
	elif igrac == 2:
		boja = BOJA_IKSA

	pygame.draw.line( displej, boja, (posX, 15), (posX, VISINA - 15),DEBLJINA_LINIJE )

def crtaj_horizontalnu_dobitnu_liniju(row, igrac):
	posY = row * VELICINA_POLJA + VELICINA_POLJA//2

	if igrac == 1:
		boja = BOJA_KRUGA
	elif igrac == 2:
		boja = BOJA_IKSA

	pygame.draw.line( displej, boja, (15, posY), (SIRINA - 15, posY), CRTA )

def crtaj_kosu_dobitnu_liniju(igrac):
	if igrac == 1:
		boja = BOJA_KRUGA
	elif igrac == 2:
		boja = BOJA_IKSA

	pygame.draw.line( displej, boja, (15, VISINA - 15), (SIRINA - 15, 15), CRTA )

def crtaj_obrnutu_kosu_dobitnu_liniju(igrac):
	if igrac == 1:
		boja = BOJA_KRUGA
	elif igrac == 2:
		boja = BOJA_IKSA

	pygame.draw.line( displej, boja, (15, 15), (SIRINA - 15, VISINA - 15), CRTA )

def restart():
	displej.fill( pozadina )
	crtaj_linije()
	for row in range(3):
		for col in range(3):
			ploca[row][col] = 0

crtaj_linije()

# ---------
# VARIABLES
# ---------
igrac = 1
game_over = False

# --------
# MAINLOOP
# --------
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

			mouseX = event.pos[0] # x
			mouseY = event.pos[1] # y

			clicked_row = int(mouseY // VELICINA_POLJA)
			clicked_col = int(mouseX // VELICINA_POLJA)

			if dostupno_polje( clicked_row, clicked_col ):

				oznaci_polje( clicked_row, clicked_col, igrac )
				if pobjeda( igrac ):
					game_over = True
				igrac = igrac % 2 + 1

				crtaj_figure()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				restart()
				igrac = 1
				game_over = False

	pygame.display.update()

