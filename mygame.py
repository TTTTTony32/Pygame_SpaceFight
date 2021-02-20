import pygame,sys,random,math
#https://www.pygame.org/docs/

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("飞机大战")
Icon = pygame.image.load("pic/logo.png")
pygame.display.set_icon(Icon)
#Images
bgImg = pygame.image.load("pic/bg.png")
HittedImg = pygame.image.load("pic/exp.png")
#BGM
pygame.mixer.music.load("sound/BGM.mp3")
pygame.mixer.music.play(-1)
#EffectSound
expsound = pygame.mixer.Sound("sound/exp.wav")
shootsound = pygame.mixer.Sound("sound/shoot.wav")

#PlayerObjects
player = pygame.image.load("pic/player.png")
playerx = 368
playery = 536
Playerstepx = 0
Playerstepy = 0
Playerstep = 5
Score = 0
Gameover = False
animate = False

#Text
WHITE = (255,255,255)
RED = (255,30,60)
GREY = (128,128,128)
font_text = pygame.font.Font('font/Minecraft-Regular.otf',30)
font_title = pygame.font.Font('font/Minecraft-Regular.otf',72)
text_over = font_title.render('GAME OVER!',False,RED)
text_quit = font_text.render('Press any key to close.',False,GREY)
def score_calc():
	text_score = font_text.render(f"Score={Score}",False,WHITE)
	screen.blit(text_score,(5,0))
def bullet_calc():
	text_bullet = font_text.render(f"Bullet={BulletNow}",False,WHITE)
	screen.blit(text_bullet,(5,35))
def game_over():
	global Gameover
	Gameover = True
	enemies1.clear()
	enemies2.clear()


#Distance
def distance(x1,y1,x2,y2):
	x = x1 - x2
	y = y1 - y2
	dis = math.sqrt(x*x + y*y)
	return dis

#Debugger
frame = 0

#Enemies
class Enemy():
	def __init__(self):
		self.img1 = pygame.image.load("pic/enemy.png")
		self.img2 = pygame.image.load("pic/enemy2.png")
		self.x = random.randint(0,735)
		self.y = random.randint(0,100)
		self.lrstep = random.randint(4,6)
		self.udstep = random.randint(1,3)
enemyNumAll = 8
enemyNum1 = random.randint(2,enemyNumAll - 3)
enemyNum2 = enemyNumAll - enemyNum1
enemies1 = []
enemies2 = []
for i in range(enemyNum1):
	enemies1.append(Enemy())
for j in range(enemyNum2):
	enemies2.append(Enemy())
def enemy_move():
	for enemy in enemies1:
		enemy.x = enemy.x + enemy.lrstep
		enemy.y = enemy.y + 0.1 * enemy.udstep
		if enemy.x > 735 or enemy.x < 0:
			enemy.lrstep = -enemy.lrstep
		if enemy.y > 540:
			game_over()
		screen.blit(enemy.img1,(enemy.x,enemy.y))
	for enemy in enemies2:
		enemy.x = enemy.x + enemy.lrstep
		enemy.y = enemy.y + 0.1 * enemy.udstep
		if enemy.x > 735 or enemy.x < 0:
			enemy.lrstep = -enemy.lrstep
		if enemy.y > 540:
			game_over()
		screen.blit(enemy.img2,(enemy.x,enemy.y))

#Bullets
class Bullet():
	def __init__(self):
		self.img = pygame.image.load("pic/Bullet.png")
		self.x = playerx
		self.y = playery
		self.step = 5
	def ifhit(self):
		global Score,BulletNow,HittedImg
		for enemy1 in enemies1:
			if distance(self.x,self.y,enemy1.x,enemy1.y) < 30:
				if self in bullets:
					bullets.remove(self)
					expsound.play()
					screen.blit(HittedImg,(enemy1.x,enemy1.y))
					pygame.display.update()
				enemy1.x = random.randint(100,740)
				enemy1.y = random.randint(-164,64)
				Score = Score - 5
				BulletNow = BulletNow + 1
		for enemy2 in enemies2:
			if distance(self.x,self.y,enemy2.x,enemy2.y) < 30:
				if self in bullets:
					bullets.remove(self)
					expsound.play()
					screen.blit(HittedImg,(enemy2.x,enemy2.y))
					pygame.display.update()
				enemy2.x = random.randint(100,740)
				enemy2.y = random.randint(-164,64)
				Score = Score + 15
				BulletNow = BulletNow - 1
BulletNum = 100
BulletNow = BulletNum
bullets = []
def bullets_show():
	for Bullet in bullets:
		Bullet.y = Bullet.y - 2 * Bullet.step
		Bullet.ifhit()
		screen.blit(Bullet.img,(Bullet.x + 15,Bullet.y))
		if Bullet.y < 0:
			if Bullet in bullets:
				bullets.remove(Bullet)

#MainGame
while True:
	#Gameover
	if BulletNow == 0:
		game_over()
	if Gameover == False:
		screen.blit(bgImg,(0,0))	#ShowBGImage
		screen.blit(player,(playerx,playery))	#ShowPlayer
	else:
		if animate == False:
			for i in range(255):
				pygame.display.update()
				screen.fill([i,i,i])
				pygame.time.delay(2)
				animate = True
		screen.blit(text_over,(200,180))	#ShowGameoverText
		screen.blit(text_quit,(210,320))
		end_score = font_text.render(f"Score={Score}",False,GREY)
		screen.blit(end_score,(330,280))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				exit()
	
	#Texts
	score_calc()
	bullet_calc()
	
	#Moves
	enemy_move()
	bullets_show()

	#Playermove
	playerx = playerx + Playerstepx
	playery = playery + Playerstepy
	if playerx > 736:
		playerx = 736
	elif playerx < 0:
		playerx = 0
	if playery > 536:
		playery = 536
	elif playery < 0:
		playery = 0
	for enemy in enemies1:
		if distance(playerx,playery,enemy.x,enemy.y) < 30:
			game_over()
	for enemy in enemies2:
		if distance(playerx,playery,enemy.x,enemy.y) < 30:
			game_over()
	#MainEvent
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		if event.type == pygame.KEYDOWN:
			#SpeedUp
			if event.key == pygame.K_LSHIFT:
				Playerstepy = 2 * Playerstepy
				Playerstepx = 2 * Playerstepx
			#Shot
			if event.key == pygame.K_SPACE:
				if BulletNow > 0:
					bullets.append(Bullet())
					BulletNow = BulletNow - 1
					shootsound.play()
			#Playermove
			if event.key == pygame.K_UP:
				Playerstepy = -Playerstep
			elif event.key == pygame.K_DOWN:
				Playerstepy = Playerstep
			if event.key == pygame.K_LEFT:
				Playerstepx = -Playerstep
			elif event.key == pygame.K_RIGHT:
				Playerstepx = Playerstep
		else:
			Playerstepx = 0
			Playerstepy = 0

	pygame.time.Clock().tick(120)
	pygame.display.update()		#RefreshView