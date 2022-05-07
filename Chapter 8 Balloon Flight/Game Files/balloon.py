import pgzrun
import pygame
import pgzrun
import random
from pgzero.builtins import Actor
from random import randint

balloon = Actor('balloon')
balloon.pos = 400, 300
bird = Actor('bird-up')
bird.pos = randint(800, 1600), randint(10, 200)
house = Actor('house')
house.pos = randint(800, 1600), 460
tree = Actor('tree')
tree.pos = randint(800, 1600), 450

WIDTH = 800
HEIGHT = 600
GRAVITY_STRENGTH = 1
bird_up = True
up = False
lives = 5 #2 Lives: added in logic for lives to keep the game going
levels = 1 #4 Level Up: added logic for leveling up to increase speed
game_over = False
score = 0
number_of_updates = 0
scores = []

def update_high_scores(): #1 More High Scores: added more numbers in .txt file for more high scores
    global score, scores
    filename = (r'C:\Users\austi\OneDrive\Documents\Class\EE104\lab8_austin_jonathan\Chapter 8 Balloon Flight\Game Files\high-scores.txt')
    scores = []
    with open(filename, 'r') as file:
        line = file.readline()
        high_scores = line.split()
        for high_score in high_scores:
            if(score > int(high_score)):
                scores.append(str(score) + ' ')
                score = int(high_score)
            else: scores.append(str(high_score) + ' ')
    with open(filename, 'w') as file: 
        for high_score in scores: file.write(high_score)

def display_high_scores():
    screen.draw.text('HIGH SCORES', (350, 150), color='black')
    y = 175
    position = 1
    for high_score in scores:
        screen.draw.text(str(position) + '.  ' + high_score, (350, y), color='black')
        y += 25
        position += 1

def draw():
    screen.blit('background', (0,0))
    if not game_over:
        balloon.draw()
        bird.draw()
        house.draw()
        tree.draw()
        screen.draw.text('Score Achieved: ' + str(score), (500, 5), color='black')
        screen.draw.text('# of Lives: ' + str(lives), (300, 5), color='black') #2 Lives: added in logic for lives to keep the game going
        screen.draw.text('Levels Passed: ' + str(levels), (100, 5), color='black') #4 Level Up: added logic for leveling up to increase speed
    else: display_high_scores()

def on_mouse_down():
    global up
    up = True
    balloon.y -= 50

def on_mouse_up():
    global up
    up = False

def flap():
    global bird_up
    if bird_up:
        bird.image = 'bird-down'
        bird_up = False
    else:
        bird.image = 'bird-up'
        bird_up = True

def update():
    global game_over, score, number_of_updates, levels, lives
    if not game_over:
        if score%10 == 0 and score != 0:
            score += 1
            levels += 1 #4 Level Up: added logic for leveling up to increase speed
        if not up: balloon.y += GRAVITY_STRENGTH
        if bird.x > 0:
            bird.x -= 5*levels #3 Speed It Up: altered obstacle speeds with level increases
            if number_of_updates == 9:
                flap()
                number_of_updates = 0
            else:
                number_of_updates += 1
        else:
            bird.x = randint(800, 1600)
            bird.y = randint(10, 200)
            score += 1
            number_of_updates = 0   
        if house.right > 0: house.x -= 3*levels #4 Level Up: added logic for leveling up to increase speed
        else:
            house.x = randint(800, 1600)
            score += 1
        if tree.right > 0: tree.x -= 3*levels #4 Level Up: added logic for leveling up to increase speed
        else:
            tree.x = randint(800, 1600)
            score += 1
        if balloon.top < 0 or balloon.bottom > 560:
            game_over = True
            update_high_scores()
        if (balloon.collidepoint(bird.x, bird.y) or balloon.collidepoint(house.x, house.y) or balloon.collidepoint(tree.x, tree.y)):
            if (lives > 1): #2 Lives: added in logic for lives to keep the game going
                bird.x = randint(800, 1600)
                bird.y = randint(10, 200)
                house.x = randint(800, 1600)
                tree.x = randint(800, 1600)
                lives -= 1
            else:
                game_over = True
                update_high_scores()

pgzrun.go()
