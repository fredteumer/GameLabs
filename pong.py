import pygame, sys
from random import randint

def load_sound(sound_name):
		try:
			sound = pygame.mixer.Sound(sound_name)
		except pygame.error, message:
			print "Cannot load sound: " + sound_name
			raise SystemExit, message
		return sound

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 20
PADDLE2_START_X = 780
PADDLE2_START_Y = 300
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
# player 2 paddle centered on right side
paddle2_rect = pygame.Rect((PADDLE2_START_X, PADDLE2_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
#middle line
midline = pygame.Rect((400, 0), (5,600))

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score = 0
score2 = 0

#2players or 1?
players = 1

#winner number
winner = 0

#gamestate
gamestate = 0

# Load the font for displaying the score
font = pygame.font.Font(None, 30)

# Game loop
while True:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		# Control the paddle with the mouse
		elif event.type == pygame.MOUSEMOTION:
			paddle_rect.centery = event.pos[1]
			# correct paddle position if it's going out of window
			if paddle_rect.top < 0:
				paddle_rect.top = 0
			elif paddle_rect.bottom >= SCREEN_HEIGHT:
				paddle_rect.bottom = SCREEN_HEIGHT
			

	# This test if up or down keys are pressed; if yes, move the paddle
	if pygame.key.get_pressed()[pygame.K_UP] and paddle_rect.top > 0:
		paddle_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle_rect.bottom < SCREEN_HEIGHT:
		paddle_rect.top += BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit(0)
		pygame.quit()
	elif pygame.key.get_pressed()[pygame.K_RETURN]:
		gamestate +=1
		
	if gamestate > 1:
		gamestate = 0
		
	if gamestate == 0:
		
		# Update ball position
		ball_rect.left += ball_speed[0]
		ball_rect.top += ball_speed[1]

		# Ball collision with rails
		if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
			ball_speed[1] = -ball_speed[1]
		if ball_rect.right >= SCREEN_WIDTH:
			ball_speed[0] = ball_speed[0]
			score += 1
			ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
			pygame.time.delay(750)
		elif ball_rect.left <= 0:
			ball_speed[0] = ball_speed[0]
			score2 +=1
			ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
			pygame.time.delay(750)
		

		# Test if the ball is hit by the paddle; if yes reverse speed and add a point
		if paddle_rect.colliderect(ball_rect):
			ball_speed[0] = -ball_speed[0]
			pew = load_sound('laser.wav')
			pew.play()
		# Test if the ball is hit by player2 paddle
		if paddle2_rect.colliderect(ball_rect):
			ball_speed[0] = -ball_speed[0]
			pew = load_sound('laser.wav')
			pew.play()
			
		if paddle2_rect.top > 0:
			paddle2_rect.top -= BALL_SPEED
		elif paddle2_rect.bottom < SCREEN_HEIGHT:
			paddle2_rect.top += BALL_SPEED
		
		if score >= 11:
			gamestate = 1
			winner = 1
		elif score2 >= 11: 
			gamestate = 1
			winner = 2
		
		paddle2_rect.top = ball_rect.top + randint(1, PADDLE_HEIGHT / 3)
	
		# Clear screen
		screen.fill((255, 255, 255))

		# Render the ball, the paddle, and the score
		pygame.draw.rect(screen, (0, 0, 0), paddle_rect) # Your paddle
		pygame.draw.rect(screen, (0, 0, 0), paddle2_rect)
		pygame.draw.rect(screen, (255, 0, 0), midline)
		pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
		score_text = font.render(str(score), True, (0, 0, 0))
		screen.blit(score_text, ((SCREEN_WIDTH / 2) - font.size(str(score))[0] / 2 - 5, 5)) # The score
		score_text2 = font.render(str(score2), True, (0, 0, 0))
		screen.blit(score_text2, ((SCREEN_WIDTH/2) + font.size(str(score2))[0] / 2 + 5, 5)) #other score
	
	elif gamestate == 1 and winner == 1:
		game = font.render("ENTER TO REPLAY", True, (0,0,0))
		screen.blit(game,((SCREEN_WIDTH/2) + 50, SCREEN_HEIGHT/2 + 50))
		p1wins = font.render("PLAYER 1 WINS!", True, (0,0,0))
		screen.blit(p1wins,((SCREEN_WIDTH/2), SCREEN_HEIGHT/2))
		score = 0
		score2 = 0
	elif gamestate == 1 and winner == 2:
		p2wins = font.render("PLAYER 2 WINS!", True, (0,0,0))
		screen.blit(p2wins,((SCREEN_WIDTH/2), SCREEN_HEIGHT/2))
		score = 0
		score2 = 0
	
	# Update screen and wait 20 milliseconds
	pygame.display.flip()
	pygame.time.delay(20)
