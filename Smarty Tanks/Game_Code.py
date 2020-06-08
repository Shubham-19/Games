import pygame
import time
import math
from random import randint

pygame.init()
clock = pygame.time.Clock()

display_width = 1400
display_height = 750

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Smarty Tanks')

destroyed, interrupted = False, False

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 200, 0)
bright_green = (0, 255, 0)
red = (200, 0, 0)
bright_red = (255, 0, 0)
yellow = (255, 255, 0)
grey = (100, 100, 100)

tankX, tankY = 1201, 635
tankX_change = 0

enemyTankX, enemyTankY = tankX, tankY
enemyTankX_change = 0

turretPos, turretPosChange = 0, 0
enemyTurretPos, enemyTurretPosChange = 0, 0

pause = True

muzzleVelocity = 100
accGravity = 10
fired = False
trackPath = False
trackEnemyPath = False
enemyFired = False

enemyTurn, playerTurn = False, True

index = 0
index_1 = 0

color = (0, 0, 0)

shellTrajectory = []
Range = 0
shellTrajectoryX, shellTrajectoryY = 0, 0

enemyShellTrajectory = []
Range = 0
enemyShellTrajectoryX, enemyShellTrajectoryY = 0, 0

rangesForEnemyTank = []

projAngle = 0

rangesForEnemyTank = []

i, j = 0, 0
count = 0
enemyTankHP, playerTankHP = 100, 100

damage, playerDamage = 0, 0

newPos = 0

gameOver = True


def text_objects(text, font, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()


def gameName():
	smallText = pygame.font.Font('freesansbold.ttf', 40)
	# color = (randint(0, 255), randint(0, 255), randint(0, 255))
	color = black
	TextSurf, TextRect = text_objects('SMARTY TANKS', smallText, color)
	TextRect.center = ((display_width/2, 60))
	gameDisplay.blit(TextSurf, TextRect)

def button(msg, x, y, w, h, inactiveColor, activeColor, action = None):
	mouse = pygame.mouse.get_pos()
	clicked = pygame.mouse.get_pressed()

	if x+w >= mouse[0] >= x and y+h >= mouse[1] >= y:
		pygame.draw.rect(gameDisplay, activeColor, (x, y, w, h))
		if clicked[0] == 1 and action != None:
			action()
	else:
		pygame.draw.rect(gameDisplay, inactiveColor, (x, y, w, h))
	smallText = pygame.font.Font('freesansbold.ttf', 20)
	TextSurf, TextRect = text_objects(msg, smallText, white)
	TextRect.center = ((x + (w/2)), (y + (h/2)))
	gameDisplay.blit(TextSurf, TextRect)


def sky(x, y):
	i, j = 0, 0
	while (0+i) <= 255:
		while j < 2*i:
			pygame.draw.line(gameDisplay, (0+i, 128+i/2, 128+i/2) , (x, y+i*2), (display_width, y+i*2))
			pygame.draw.line(gameDisplay, (0+i, 128+i/2, 128+i/2) , (x, y+i*2+1), (display_width, y+i*2+1))
			j += 1
		i += 1


def cloud(x, y):
	size = 30
	pygame.draw.circle(gameDisplay, (100, 100, 100), (x, y), size)
	pygame.draw.circle(gameDisplay, (200, 200, 200), (x+25, y-10), size)
	pygame.draw.circle(gameDisplay, (255, 255, 255), (x+75, y), size)
	pygame.draw.circle(gameDisplay, (150, 150, 150), (x+50, y-10), size)
	pygame.draw.circle(gameDisplay, (255, 255, 255), (x+25, y+10), size)
	pygame.draw.circle(gameDisplay, (200, 200, 200), (x+50, y+10), size)

	
def ground():
	gameDisplay.fill((0, 50, 0), rect = [0, 670, display_width, display_height])
	gameDisplay.fill((150, 128, 0), rect = [0, 670, display_width, 20])
	gameDisplay.fill((0, 150, 0), rect = [0, 670+20, display_width, 5])
	gameDisplay.fill((0, 150, 0), rect = [0, 670+30, display_width, 5])
	gameDisplay.fill((0, 150, 0), rect = [0, 670+40, display_width, 5])


def drawAfterEffects(x, y):
	if (display_width-enemyTankX + 150) > x > (display_width-(enemyTankX+int(125*0.5))):
		for i in range(1):
			pygame.draw.circle(gameDisplay, (randint(125, 255), 150, 0), (randint(x+25, x+35), randint(y-50, y-10)), 5)
			pygame.draw.circle(gameDisplay, (randint(125, 255), 255, 0), (randint(x-35, x-25), randint(y+10, y+50)), 5)
			pygame.draw.circle(gameDisplay, (randint(125, 255), 150, 0), (randint(x+25, x+35), randint(y+10, y+50)), 5)
			pygame.draw.circle(gameDisplay, (randint(125, 255), 255, 0), (randint(x-35, x-25), randint(y-50, y-10)), 5)
			pygame.draw.circle(gameDisplay, (randint(125, 255), 255, 0), (x, randint(y+10, y+50)), 5)
			pygame.draw.circle(gameDisplay, (randint(125, 255), 255, 0), (x, randint(y-50, y-10)), 5)


def showShell(shellTrajectory):
	global index, fired
	if index < len(shellTrajectory):
		pygame.draw.circle(gameDisplay, black, shellTrajectory[index], 10)
		drawAfterEffects(shellTrajectory[index-10][0], shellTrajectory[index-10][1])
	
		index += 10
	else:
		fireShell(shellTrajectory)
		# enemyTurn = True
		playerTurn = False
		fired = False

	
def showEnemyShell(enemyShellTrajectory):
	global index_1, playerTurn, enemyTurn, trackEnemyPath, fired
	# trackEnemyPath = False
	if index_1 < len(enemyShellTrajectory):

		pygame.draw.circle(gameDisplay, black, enemyShellTrajectory[index_1], 10)
		
		index_1 += 10
	else:
		enemyFiresShell(enemyShellTrajectory)
		playerTurn = True
		enemyTurn = False


damage = 0
def fireShell(shellTrajectory):
	global index, damage, enemyTankHP, enemyTurn

	if (display_width-(enemyTankX))  > shellTrajectory[index-10][0] and (display_width-(enemyTankX+int(125*0.5))) < shellTrajectory[index-10][0]:
		print('Target Hit!')
		damage = 20
	else:
		damage = 0
	enemyTankHP -= damage
	if enemyTankHP == 0:
		gameFinished()
	enemyTurn = True
	index = 0


playerDamage = 0
def enemyFiresShell(enemyShellTrajectory):
	global index_1, playerDamage, playerTankHP, enemyFired, trackEnemyPath
	if (tankX  < enemyShellTrajectory[index_1-10][0] and (tankX+int(125*0.5)) >= enemyShellTrajectory[index_1-10][0]):
		print('Target Hit!')
		playerDamage = 20
	else:
		playerDamage = 0
	playerTankHP -= playerDamage
	if playerTankHP == 0:
		gameFinished()
	index_1 = 0
	# enemyFired == False
	
			
def drawPath(x, y, Range, shellTrajectory, possiblePositionForTurret):
	for value in shellTrajectory:
		# print(value, enemyTurretPos, possiblePositionForTurret[turretPos][0])
		if (x+int(75*0.5)-int(Range*0.2)) < value[0] < possiblePositionForTurret[turretPos][0]:
			pygame.draw.circle(gameDisplay, red, value, 3)


def drawEnemyPath(x, y, enemyShellTrajectory, possiblePositionForEnemyTurret):
	global enemyFired, trackEnemyPath
	for value in enemyShellTrajectory:
		# print(value, enemyTurretPos, possiblePositionForEnemyTurret[enemyTurretPos][0], (display_width - (x+int(75*0.5))+max(rangesForEnemyTank)))
		if possiblePositionForEnemyTurret[enemyTurretPos][0] < value[0] < (display_width - (x+int(75*0.5))+max(rangesForEnemyTank)):
			pygame.draw.circle(gameDisplay, red, value, 3)


def enemyTankHealthPoints(enemyTankHP):
	smallText = pygame.font.Font('freesansbold.ttf', 20)
	if 100 >= enemyTankHP >= 70:
		color = green
	elif 40 <= enemyTankHP < 70:
		color = yellow
	elif 0 <= enemyTankHP < 40:
		color = red
	else:
		enemyTankHP = 0
		color = red
	TextSurf, TextRect = text_objects(str(enemyTankHP), smallText, color)
	TextRect.center = (50, 35)
	gameDisplay.blit(TextSurf, TextRect)
	s = pygame.Surface((200, 25))
	s.set_alpha(128)
	s.fill(white)
	gameDisplay.blit(s, (25, 50))
	pygame.draw.rect(gameDisplay, color, (25, 50, 2*enemyTankHP, 25))


def playerTankHealthPoints(playerTankHP):
	smallText = pygame.font.Font('freesansbold.ttf', 20)
	if 100 >= playerTankHP >= 70:
		color = green
	elif 40 <= playerTankHP < 70:
		color = yellow
	else:
		color = red
	TextSurf, TextRect = text_objects(str(playerTankHP), smallText, color)
	TextRect.center = (1350, 35)
	gameDisplay.blit(TextSurf, TextRect)
	s = pygame.Surface((200, 25))
	s.set_alpha(128)
	s.fill(white)
	gameDisplay.blit(s, (1175, 50))
	# pygame.draw.rect(gameDisplay, (255, 255, 255, 50), (25, 50, 200, 25))
	pygame.draw.rect(gameDisplay, color, (1175, 50, 2*playerTankHP, 25))


def shellRange(x, y, possiblePositionForTurret):
	global shellTrajectory, fired, trackPath, index, Range, projAngle, shellTrajectoryX, shellTrajectoryY, enemyTurn, playerTurn, playerShellRangesForTurretPos
	if trackPath == True:
		shellTrajectory = []
		shellTrajectoryX, shellTrajectoryY = x, y
		# print(possiblePositionForTurret[enemyTurretPos][0] - (x+int(75*0.5)), possiblePositionForTurret[enemyTurretPos][1] - y)
		projAngle = math.atan((possiblePositionForTurret[turretPos][1] - y)/(possiblePositionForTurret[turretPos][0] - (x+int(75*0.5))))
		Range = 2*((muzzleVelocity*math.sin(projAngle))*(muzzleVelocity*math.cos(projAngle)))/accGravity
		maxHeight = Range*math.tan(projAngle)/4
			
		# print(projAngle, Range, maxHeight)
		for i in range(x+int(75*0.5), x-int(Range), -1):

			# print(i, possiblePositionForTurret[turretPos][0])
			shellTrajectoryX = x+int(75*0.5)-i
			shellTrajectoryY = shellTrajectoryX*math.tan(projAngle) - ((accGravity*(shellTrajectoryX)**2)/(2*(muzzleVelocity**2)*(math.cos(projAngle))**2))
			shellTrajectory.append((i, y-int(shellTrajectoryY)))	
		 
		# print(shellTrajectory)

		drawPath(x, y, Range, shellTrajectory, possiblePositionForTurret)

	if fired == True:

		showShell(shellTrajectory)
		# playerTurn = False
		# enemyTurn = True


def enemyShellRange(x, y, possiblePositionForEnemyTurret):
	global enemyShellTrajectory, enemyFired, trackEnemyPath, index_1, Range, projAngle, enemyShellTrajectoryX, enemyShellTrajectoryY, enemyTurn, playerTurn

	enemyShellTrajectory = []
	enemyShellTrajectoryX, enemyShellTrajectoryY = display_width - x, y

	for i in range(display_width - (x+int(75*0.5)), display_width - (x+int(75*0.5)) + max(rangesForEnemyTank), 1):

		# print(i, possiblePositionForTurret[turretPos][0])
		enemyShellTrajectoryX = i - (display_width - (x+int(75*0.5)))
		enemyShellTrajectoryY = enemyShellTrajectoryX*math.tan(projAngle) - ((accGravity*(enemyShellTrajectoryX)**2)/(2*(muzzleVelocity**2)*(math.cos(projAngle))**2))
		# print(enemyShellTrajectoryX, enemyShellTrajectoryY)
		enemyShellTrajectory.append((i, y-int(enemyShellTrajectoryY)))	
	# print(enemyShellTrajectory)
	# drawEnemyPath(x, y, enemyShellTrajectory, possiblePositionForEnemyTurret)

	if enemyFired == True:
		showEnemyShell(enemyShellTrajectory)
		# enemyFiresShell(enemyShellTrajectory)


def findEnemyTurretPosition(x, y):
	global possiblePositionForEnemyTurret

	possiblePositionForEnemyTurret = [(display_width-(x-int(27*0.5)), y-int(2*0.5)),
								 (display_width-(x-int(26*0.5)), y-int(5*0.5)),
								 (display_width-(x-int(25*0.5)), y-int(8*0.5)),
								 (display_width-(x-int(23*0.5)), y-int(12*0.5)),
								 (display_width-(x-int(20*0.5)), y-int(14*0.5)),
								 (display_width-(x-int(18*0.5)), y-int(15*0.5)),
								 (display_width-(x-int(15*0.5)), y-int(17*0.5)),
								 (display_width-(x-int(13*0.5)), y-int(19*0.5)),
								 (display_width-(x-int(11*0.5)), y-int(21*0.5)),
								 (display_width-(x+int(9*0.5)), y-int(40*0.5)),
								 (display_width-(x+int(10*0.5)), y-int(45*0.5)),
								 (display_width-(x+int(11*0.5)), y-int(50*0.5)),
								 (display_width-(x+int(12*0.5)), y-int(50*0.5)),
								 (display_width-(x+int(13*0.5)), y-int(50*0.5)),
								 (display_width-(x+int(27*0.5)), y-int(50*0.5)),
								 (display_width-(x+int(50*0.5)), y-int(55*0.5))
								 ]


def gameBOT(x, y):
	global projAngle, Range, rangesForEnemyTank, enemyTankX, enemyTankX_change, newPos
	rangesForEnemyTank = []
	projAngleArr = []
	findEnemyTurretPosition(x, y)
	for position in possiblePositionForEnemyTurret:
		# print(position[0], display_width-(x-int(75*0.5)))
		# print((y - position[1]), (position[0] - (display_width - (x+int(75*0.5)))))
		projAngle = math.atan((y - position[1])/(position[0] - (display_width - (x+int(75*0.5)))))
		Range = 2*((muzzleVelocity*math.sin(projAngle))*(muzzleVelocity*math.cos(projAngle)))/accGravity
		projAngleArr.append(projAngle*180/math.pi)
		rangesForEnemyTank.append(int(Range))
		projAngle = projAngleArr[rangesForEnemyTank.index(max(rangesForEnemyTank))]*math.pi/180
	
	newPos = ((x + int(75*0.5)) - max(rangesForEnemyTank))


def moveBot():
	global enemyTankX, enemyTankX_change, enemyTurretPos, trackEnemyPath, enemyFired
	pos, finalTurretPos = 0, 0

	if enemyTurn == True:
		# print(enemyTankX + 1, enemyTankX - 1, newPos, display_width - (enemyTank,X + int(75*0.5)))
		if newPos > display_width - (enemyTankX + int(75*0.5)):
			enemyTankX_change -= 1
		elif newPos < display_width - (enemyTankX + int(75*0.5)):
			enemyTankX_change += 1
		else:
			enemyTankX_change = 0
			enemyTurretPos = rangesForEnemyTank.index(max(rangesForEnemyTank))

			# trackEnemyPath = True
			enemyFired = True
			enemyShellRange(enemyTankX, enemyTankY, possiblePositionForEnemyTurret)

def Tank(x, y, turretPos):
	global possiblePositionForTurret, projAngle, playerTurn, enemyTurn

	possiblePositionForTurret = [(x-int(27*0.5), y-int(2*0.5)),
								 (x-int(26*0.5), y-int(5*0.5)),
								 (x-int(25*0.5), y-int(8*0.5)),
								 (x-int(23*0.5), y-int(12*0.5)),
								 (x-int(20*0.5), y-int(14*0.5)),
								 (x-int(18*0.5), y-int(15*0.5)),
								 (x-int(15*0.5), y-int(17*0.5)),
								 (x-int(13*0.5), y-int(19*0.5)),
								 (x-int(11*0.5), y-int(21*0.5)),
								 (x+int(9*0.5), y-int(40*0.5)),
								 (x+int(10*0.5), y-int(45*0.5)),
								 (x+int(11*0.5), y-int(50*0.5)),
								 (x+int(12*0.5), y-int(50*0.5)),
								 (x+int(13*0.5), y-int(50*0.5)),
								 (x+int(27*0.5), y-int(50*0.5)),
								 (x+int(50*0.5), y-int(55*0.5))
								 ]

	# print(possiblePositionForTurret)
	# pygame.draw.line(gameDisplay, black, (x+int(75*0.5), y), (possiblePositionForTurret[turretPos][0], possiblePositionForTurret[turretPos][1]), 5)
	pygame.draw.line(gameDisplay, black, (x+int(75*0.5), y), (possiblePositionForTurret[turretPos][0], possiblePositionForTurret[turretPos][1]), int(5*0.5))

	# pygame.draw.circle(gameDisplay, blue, (x+int(75*0.5), y+25), 45)
	pygame.draw.circle(gameDisplay, black, (x+int(75*0.5), y+int(10*0.5)), int(20*0.5))
	pygame.draw.polygon(gameDisplay, black, [(x+int(25*0.5), y), (x-int(20*0.5), y+int(50*0.5)), (x+int(170*0.5), y+int(50*0.5)), (x+int(125*0.5), y)])
	# pygame.draw.rect(gameDisplay, black, (x, y, 150, 50))
	wx, wy = x, y+int(50*0.5)
	for i in range(4):
		pygame.draw.circle(gameDisplay, black, ((wx+int(i*40*0.5)), wy), int(20*0.5))
		# pygame.draw.circle(gameDisplay, black, ((wx + 20), wy), 20)
		wx += int(10*0.5)

	pygame.draw.line(gameDisplay, black, (x, y+int(67*0.5)), (x+int(150*0.5), y+int(67*0.5)), int(5*0.5))

	shellRange(x, y, possiblePositionForTurret)
	

def enemyTank(x, y, turretPos):
	global possiblePositionForEnemyTurret, enemyTurn, playerTurn
	possiblePositionForEnemyTurret = [(display_width-(x-int(27*0.5)), y-int(2*0.5)),
								 (display_width-(x-int(26*0.5)), y-int(5*0.5)),
								 (display_width-(x-int(25*0.5)), y-int(8*0.5)),
								 (display_width-(x-int(23*0.5)), y-int(12*0.5)),
								 (display_width-(x-int(20*0.5)), y-int(14*0.5)),
								 (display_width-(x-int(18*0.5)), y-int(15*0.5)),
								 (display_width-(x-int(15*0.5)), y-int(17*0.5)),
								 (display_width-(x-int(13*0.5)), y-int(19*0.5)),
								 (display_width-(x-int(11*0.5)), y-int(21*0.5)),
								 (display_width-(x+int(9*0.5)), y-int(40*0.5)),
								 (display_width-(x+int(10*0.5)), y-int(45*0.5)),
								 (display_width-(x+int(11*0.5)), y-int(50*0.5)),
								 (display_width-(x+int(12*0.5)), y-int(50*0.5)),
								 (display_width-(x+int(13*0.5)), y-int(50*0.5)),
								 (display_width-(x+int(27*0.5)), y-int(50*0.5)),
								 (display_width-(x+int(50*0.5)), y-int(55*0.5))
								 ]

	# print(possiblePositionForTurret)
	pygame.draw.line(gameDisplay, black, (display_width-(x+int(75*0.5)), y), (possiblePositionForEnemyTurret[enemyTurretPos][0], possiblePositionForEnemyTurret[enemyTurretPos][1]), int(5*0.5))
	# pygame.draw.circle(gameDisplay, blue, (x+int(75*0.5), y+25), 45)
	pygame.draw.circle(gameDisplay, black, (display_width-(x+int(75*0.5)), y+int(10*0.5)), int(20*0.5))
	pygame.draw.polygon(gameDisplay, black, [(display_width-(x+int(25*0.5)), y), (display_width-(x-int(20*0.5)), y+int(50*0.5)), (display_width-(x+int(170*0.5)), y+int(50*0.5)), (display_width-(x+int(125*0.5)), y)])
	# pygame.draw.rect(gameDisplay, black, (x, y, 150, 50))
	wx, wy = x, y+int(50*0.5)
	for i in range(4):
		pygame.draw.circle(gameDisplay, black, ((display_width-(wx+int(i*40*0.5))), wy), int(20*0.5))
		# pygame.draw.circle(gameDisplay, black, ((wx + 20), wy), 20)
		wx += int(10*0.5)
	
	pygame.draw.line(gameDisplay, black, (display_width-x, y+int(67*0.5)), (display_width-(x+int(150*0.5)), y+int(67*0.5)), int(5*0.5))
	# projAngle = math.atan((possiblePositionForEnemyTurret[turretPos][1] - y)/((display_width-possiblePositionForEnemyTurret[turretPos][0]) - (x+int(75*0.5))))
	
	# enemyShellRange(x, y, possiblePositionForEnemyTurret)

	
def gameQuit():
	pygame.quit()
	quit()


def gameIntro():
	tankImage = pygame.image.load('Tank_1.png')
	x, y = display_width/2, display_height/2
	while not interrupted:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
	
		gameDisplay.fill(black)

		largeText = pygame.font.Font('C:/Windows/Fonts/AstronBoyWonder.ttf', 115)
		TextSurf, TextRect = text_objects('SMARTY TANKS', largeText, white)
		TextRect.center = ((display_width/2), (display_height/4))
		gameDisplay.blit(TextSurf, TextRect)
		gameDisplay.blit(tankImage, (x, y))

		if x+657 < 0:
			button('Play', display_width/3, display_height/2, 100, 50, green, bright_green, gameLoop)
			button('Quit', (display_width/3)*2, display_height/2, 100, 50, red, bright_red,gameQuit)

		pygame.display.update()
		x -= 2
		

def unpause():
	global pause
	pause = False

def gamePaused():
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
	
		gameDisplay.fill(black)

		largeText = pygame.font.Font('freesansbold.ttf', int(75*0.5))
		TextSurf, TextRect = text_objects('GAME PAUSED....', largeText, white)
		TextRect.center = ((display_width/2), (display_height/4))
		gameDisplay.blit(TextSurf, TextRect)
		
		button('Continue', display_width/3, display_height/2, 100, 50, green, bright_green, unpause)
		button('Quit', (display_width/3)*2, display_height/2, 100, 50, red, bright_red,gameQuit)

		pygame.display.update()


def restartGame():
	global tankX, tankY, tankX_change, enemyTankX, enemyTankY, enemyTankX_change, turretPos, turretPosChange, enemyTurretPos, enemyTurretPosChange
	global pause, fired, i, j, projAngle, index, index_1, trackPath, Range, enemyTurn, playerTurn, playerDamage, gameOver, pause
	global destroyed, damage, possiblePositionForTurret, shellTrajectory, enemyTankHP, count, playerTankHP, enemyShellTrajectory, enemyFired, trackEnemyPath
	global display_width, display_height, gameDisplay, interrupted, white, black, blue, green, bright_red, bright_green, grey, yellow
	global muzzleVelocity, accGravity, color

	display_width = 1400
	display_height = 750

	gameDisplay = pygame.display.set_mode((display_width, display_height))
	pygame.display.set_caption('Smarty Tanks')

	destroyed, interrupted = False, False

	white = (255, 255, 255)
	black = (0, 0, 0)
	blue = (0, 0, 255)
	green = (0, 200, 0)
	bright_green = (0, 255, 0)
	red = (200, 0, 0)
	bright_red = (255, 0, 0)
	yellow = (255, 255, 0)
	grey = (100, 100, 100)

	tankX, tankY = 1200, 635
	tankX_change = 0

	enemyTankX, enemyTankY = tankX, tankY
	enemyTankX_change = 0

	turretPos, turretPosChange = 0, 0
	enemyTurretPos, enemyTurretPosChange = 0, 0

	pause = True

	muzzleVelocity = 100
	accGravity = 10
	fired = False
	trackPath = False
	trackEnemyPath = False
	enemyFired = False

	enemyTurn, playerTurn = False, True

	index = 0
	index_1 = 0

	color = (0, 0, 0)

	shellTrajectory = []
	Range = 0
	shellTrajectoryX, shellTrajectoryY = 0, 0

	enemyShellTrajectory = []
	Range = 0
	enemyShellTrajectoryX, enemyShellTrajectoryY = 0, 0

	possiblePositionForTurret = []

	projAngle = 0

	rangesForEnemyTank = []

	i, j = 0, 0
	count = 0
	enemyTankHP, playerTankHP = 100, 100

	damage, playerDamage = 0, 0

	newPos = 0

	gameOver = False

	gameLoop()


def gameFinished():
	global gameOver, destroyed
	# destroyed = True
	while gameOver:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(black)

		largeText = pygame.font.Font('freesansbold.ttf', 75)
		if enemyTankHP > playerTankHP:
			TextSurf, TextRect = text_objects('Computer Wins...', largeText, white)
		else:
			TextSurf, TextRect = text_objects('Player Wins...', largeText, white)
		TextRect.center = ((display_width/2), (display_height/4))
		gameDisplay.blit(TextSurf, TextRect)

		button('Play Again', display_width/3, display_height/2, 150, 50, green, bright_green, restartGame)
		button('Quit', (display_width/3)*2, display_height/2, 150, 50, red, bright_red,gameQuit)

		pygame.display.update()
		
		
def gameLoop():
	global tankX, tankY, tankX_change, enemyTankX, enemyTankY, enemyTankX_change, turretPos, turretPosChange, enemyTurretPos, enemyTurretPosChange
	global pause, fired, i, j, projAngle, index, index_1, trackPath, Range, enemyTurn, playerTurn, playerDamage, gameOverd
	global destroyed, damage, possiblePositionForTurret, shellTrajectory, enemyTankHP, count, playerTankHP, enemyShellTrajectory, enemyFired, trackEnemyPath
	
	
	while not destroyed:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if playerTurn == True:
					if event.key == pygame.K_LEFT:
						tankX_change -= 5
					if event.key == pygame.K_RIGHT:
						tankX_change += 5
					if event.key == pygame.K_UP:
						turretPosChange += 1
					if event.key == pygame.K_DOWN:
						turretPosChange -= 1
					if event.key == pygame.K_SPACE:
						fired = True
						gameBOT(tankX, tankY)
						# enemyTurn = True
						playerTurn = False
						# enemyTankHP -= damage
						# if enemyTankHP == 0:
						# 	gameOver = True
						# 	gameFinished()
						trackPath = False						
					if event.key == pygame.K_t:
						trackPath = True
						fired = False
						index = 0
				if event.key == pygame.K_p:
					pause = True
					gamePaused()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					tankX_change = 0
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					turretPosChange = 0
				if event.key == pygame.K_a or event.key == pygame.K_d:
					enemyTankX_change = 0
				if event.key == pygame.K_w or event.key == pygame.K_s:
					enemyTurretPosChange = 0


		turretPos += turretPosChange
		
		if turretPos > 15:
			turretPos = 15
		if turretPos < 0:
			turretPos = 0
		if enemyTurretPos > 15:
			enemyTurretPos = 15
		if enemyTurretPos < 0:
			enemyTurretPos = 0

		tankX += tankX_change		

		gameDisplay.fill((255,255,255))
		
		sky(0, 0)
		gameName()

		
		if i*3 > display_width:
			cloud(0+i*3,100)
			i = 0
			count = 0
		if i*3 < display_width:
			cloud(0+i*3, 100)
			i += 1
		if j*2 > display_width:
			cloud(display_width - (j*2), 100)
			j = 0
			count = 0
		if j*2 >= 0:
			cloud(display_width - (j*2), 100)
			j += 1
		if (i*3 >= (display_width - (j*2)) or (display_width - (i*3)) <= j*2) and count == 0:
			count = 1
			gameDisplay.fill(black)
		
		# print(display_width-(i*3), j)
		# print(i, display_width - j)
		# print(i*3, display_width - (j*2), j*2, display_width - (i*3))

	
		enemyTankHealthPoints(enemyTankHP)
		playerTankHealthPoints(playerTankHP)
		Tank(tankX, tankY, turretPos)
		moveBot()
		enemyTankX += enemyTankX_change
		enemyTank(enemyTankX, enemyTankY, enemyTurretPos)
		ground()
		enemyTankX_change = 0
		pygame.display.update()
		clock.tick(60)
		

# gameIntro()
gameLoop()
pygame.quit()
quit()
