from p5 import *
from random import randint, uniform
from math import pi as PI, cos, sin, degrees

WIDTH = 1000
HEIGHT = 600
score_a = 0
score_b = 0

def left_wall(obj):
	global pong_ball, score_b
	# override old ball
	score_b += 1
	pong_ball = Ball()
	print("Player B gained a point! \nCurrently A {} - {} B".format(score_a, score_b))

def right_wall(obj):
	global pong_ball, score_a
	# override old ball
	pong_ball = Ball()
	score_a += 1
	print("Player A gained a point! \nCurrently A {} - {} B".format(score_a, score_b))


class Ball():
	def __init__(self, x=WIDTH/2, y=HEIGHT/2, d=20, min_init_speed=5, max_init_speed=5):
		def start_angle():
			angle = uniform(0, 2*PI)
			# we don't want to init at sky-high angles (cos(60)=0.5)
			while cos(angle)<0.5 and cos(angle)>-0.5:
				angle = uniform(0, 2*PI)

			return angle

		self.x = x
		self.y = y
		self.speed = randint(min_init_speed, max_init_speed)
		
		self.angle = start_angle()
		# trigonometric speeds
		self.v_x = self.speed*cos(self.angle)
		self.v_y = self.speed*sin(self.angle)

		self.d = d
		self.pos = [self.x, self.y]
		self.v = [self.v_x, self.v_y]

	def update_pos(self):
		self.x += self.v_x
		self.y += self.v_y
		self.pos = [self.x, self.y] # center of bars

		# ball and player_a collision, between top and bottom of bar, if on left side
		if (self.x-self.d/2 <= player_a.x+player_a.fatness/2 and \
			(self.y < player_a.y+player_a.longness/2 and self.y > player_a.y-player_a.longness)):

			self.v_x *= -1.1
			self.v_y = uniform(0, 2*PI)
			self.v = [self.v_x, self.v_y]
			print("mod_v:", sqrt(self.v_x**2 + self.v_y**2))
			print("x:", self.v_x)

		# ball and player_b collision, between top and bottom of bar, if on right side
		elif(self.x+self.d/2 >= player_b.x-player_b.fatness/2 and \
			(self.y < player_b.y+player_b.longness/2 and self.y > player_b.y-player_b.longness)):

			self.v_x *= -1.1
			self.v_y = uniform(0, 2*PI)
			self.v = [self.v_x, self.v_y]
			print("mod_v", sqrt(self.v_x**2 + self.v_y**2))
			print("x:", self.v_x)


		# lose at wall
		if self.x+self.d/2 >= WIDTH:
			right_wall(self)
		elif self.x-self.d/2 <= 0:
			left_wall(self)

		# roof and floor
		if self.y+self.d/2 >= HEIGHT:
			self.y = HEIGHT-self.d/2
			self.v_y *= -1
		if self.y-self.d/2 < 0:
			self.y = self.d/2
			self.v_y *= -1


class Bar():
	def __init__(self, x, y=HEIGHT/2, fatness=7, longness=50):
		self.x = x
		self.y = y
		self.fatness = fatness # decoration, really
		self.longness = longness # difficulty?

		self.pos = [self.x, self.y] # center of bars
		self.size = [self.fatness, self.longness]

		self.v_y = 0

	def update_pos(self):
		# reset speed on end of field
		if self.v_y > 0 and self.y+self.longness/2 >= HEIGHT:
			self.v_y = 0
		if self.v_y < 0 and self.y-self.longness/2 <= 0:
			self.v_y = 0

		# move!
		self.y += self.v_y

		# force bar into gamefield
		if self.y-self.longness/2 < 0:
			self.y = self.longness/2
		elif self.y+self.longness/2 > HEIGHT:
			self.y = HEIGHT-self.longness/2

		self.pos = [self.x, self.y]


def setup():
	size(WIDTH, HEIGHT)
	no_stroke()

speed_colours = {
	0: Color(170,170,170),
	2: Color(255,255,255),
	4: Color(255,165,0),
	6: Color(255,140,0),
	8: Color(255,99,70),
	10: Color(255,69,0),
	12: Color(255,0,0),
	-2: Color(255,255,255),
	-4: Color(255,165,0),
	-6: Color(255,140,0),
	-8: Color(255,99,70),
	-10: Color(255,69,0),
	-12: Color(255,0,0)
}

def draw(): 
	#text_font(avenir_font)
	background(0) # black
	fill(255, 255, 255) # white

	# ball
	circle(pong_ball.pos, pong_ball.d)

	# bars
	fill(speed_colours[player_a.v_y])
	rect(player_a.pos, *player_a.size, mode="CENTER")

	fill(speed_colours[player_b.v_y])
	rect(player_b.pos, *player_b.size, mode="CENTER")

	fill(255, 255, 255)
	# update their pos (velocity impact)
	for obj in [player_a, player_b, pong_ball]:
		obj.update_pos()

	stroke(255, 255, 255)
	for small_line in range(100, HEIGHT-20, 10):
		line((WIDTH/2, small_line), (WIDTH/2, small_line+5))


	# adding stars for score tracking
	diametre_star = 10
	margin = diametre_star*2 # not really margin, rather offset
	allocated_space = WIDTH/2 -20*2 # 20 margin per side
	stars_per_row = allocated_space/margin

	stars_a_added = 0
	for point in range(score_a):
		position_star = [20+(point%stars_per_row)*margin, 20+stars_a_added//stars_per_row*margin]
		circle(position_star, diametre_star)
		stars_a_added += 1

	stars_b_added = 0
	for point in range(score_b):
		position_star = [WIDTH-(20+(point%stars_per_row)*margin), 20+stars_b_added//stars_per_row*margin]
		circle(position_star, diametre_star)
		stars_b_added += 1


def key_pressed():
	# each press adds more speed!
	if key == "W":
		player_a.v_y += -2
	if key == "S":
		player_a.v_y += 2
	if key == "UP":
		player_b.v_y += -2
	if key == "DOWN":
		player_b.v_y += 2

pong_ball = Ball()
player_a = Bar(20)
player_b = Bar(WIDTH - 20)
run(frame_rate=120)