from tkinter import *
from tkinter import messagebox
from random import randint
from threading import Thread
from time import sleep

last_pos = None

# On game start settings.
direction = 'DOWN'
last_step = 'UP'
score = 0

# Status for pauses or game stops.
game_status = 'OFF'

# n - field size; pixel_width - width for tkinter Frames in field;
n = 20
pixel_width = 20

# Creating main window.
window = Tk()
window.geometry('{0}x{1}'.format(str(pixel_width*n), str(pixel_width*n+20)))
window.resizable(False, False)
window.title('Snake by psisuk24')


# Creating field array with Frames of tkinter as pixels.
def field_create():
	global field
	field = []
	for y in range(n):
		field.append([])
		for x in range(n):
			field[y].append(Frame(window, width=pixel_width, height=pixel_width, bg='black'))
			field[y][x].grid(column=x, row=y)


# Creating snake's head in random place.
def player_create(field):
	global snake
	y = randint(0, n-1)
	x = randint(0, n-1)
	snake = [[y, x]]
	field[y][x].config(bg='lime') #Coloring snake's head.
	return field


# Creating an apple in random place.
def apple_create(field):
	global apple_y, apple_x
	apple_y = randint(0, n-1)
	apple_x = randint(0, n-1)
	while [apple_y, apple_x] in snake: # Little loop for 'apple in snake's body spawn' bug fix.
		apple_y = randint(0, n-1)
		apple_x = randint(0, n-1)
	field[apple_y][apple_x].config(bg='red') # Coloring an apple.


# Main logic for one actual frame.
def tick():
	global field, apple_y, apple_x, snake, last_pos, score

	# Cheking for apple bite.
	if snake[0][0] == apple_y and snake[0][1] == apple_x:
		apple_create(field)
		score += 100
		snake.append([0, 0])

	# Replacing snake's tail after head.
	if len(snake)-1 >= 1:
		snake.insert(1, last_pos)
		snake.pop(len(snake)-1)

		# Cheking for snake's self bite.
		if snake[0] in snake[1:]:
			game_stop()
			messagebox.showinfo('Game over.', 'Game is over! Your score: ' + str(score))
			restore()

	# Drawing field loop.
	for i in range(n):
		for j in range(n):
			if [i, j] == snake[0]:
				field[i][j].config(bg='lime')
			elif [i, j] in snake:
				field[i][j].config(bg='green')
			elif [i, j] == [apple_y, apple_x]:
				field[i][j].config(bg='red')
			else: field[i][j].config(bg='black')

	# Saving last snake's head position for the next iteration.
	last_pos = [snake[0][0], snake[0][1]]

	# Updating score label.
	label_score.config(text='Счет: ' + str(score))

	# Slowing game down.
	sleep(0.05)


# Changing direction.
def direction_change(event):
	global direction
	# Not letting snake move in opposite direction.
	if event.keycode == 68 and last_step != 'LEFT':
		direction = 'RIGHT'
	elif event.keycode == 65 and last_step != 'RIGHT':
		direction = 'LEFT'
	elif event.keycode == 87 and last_step != 'DOWN':
		direction = 'UP'
	elif event.keycode == 83 and last_step != 'UP':
		direction = 'DOWN'


# Moving snake's head.
def move():
	global game_status
	global snake, last_step
	while game_status == 'ON':
		if direction == 'RIGHT':
			snake[0][1] += 1
		elif direction == 'LEFT':
			snake[0][1] -= 1
		elif direction == 'UP':
			snake[0][0] -= 1
		elif direction == 'DOWN':
			snake[0][0] += 1

		# Not letting snake get out of field.
		if snake[0][0] > n-1:
			snake[0][0] -= n
		elif snake[0][0] < 0:
			snake[0][0] += n

		if snake[0][1] > n-1:
			snake[0][1] -= n
		elif snake[0][1] < 0:
			snake[0][1] += n

		# Saving last step direction for correct direction change.
		last_step = direction

		tick()


# Starting game.
def game_start(event=None):
	global game_status
	if game_status != 'ON':
		game_status = 'ON'
		move_thread = Thread(target=move)
		move_thread.start()
	else: return False


# Function for Restore score and snake.
def restore():
	global score
	player_create(field)
	apple_create(field)
	score = 0


# Stopping game.
def game_stop(event=None):
	global game_status, snake
	game_status = 'OFF'


# Binds.
window.bind('<Key>', direction_change) # Direction change on [ W, A, S, D ].
window.bind('<Return>', game_start) # Start on Enter.
window.bind('<Escape>', game_stop) # Pause on Esc.

# Score Label.
label_score = Label(width=20, height=0, text='Счет: ')
label_score.grid(column=0, columnspan=n, row=n+1, sticky='w')


# Starting program.
field_create()
player_create(field)
apple_create(field)
window.mainloop()
