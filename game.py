#"River Run" by Wyatt O'Connell (qdy5bq)
# A player's score accumulates over time
# the game's perspective is a bird's eye view of the river and the kayaker
# the user presses the left and right arrow keys to paddle

#MANDATORY FEATURES

#User Input:
#The kayaker will be controlled by the left and right arrow keys
# The left arrow will represent a left-side paddle stroke and vice versa on the right
# with each stroke, the kayaker moves forward and slightly to the side, making it challenging to navigate obstacles

#Start Screen
# before the game starts there will be a starting screen that will display a high score, instructions, and a strat button, the start button will disappear when clicked

#Game Over
# the game will end when the kayaker's health bar decreases to zero

#Small Enough Window
# our window will be small enough

#Graphics/Images
# the kayaker, two different types of rocks, and fish will be represented by images
# we will include them with submission

#OPTIONAL FEATURES

#Collectibles
# the kayaker will be able to collect fish peaking out of the water to refill their health bar

#Health Bar
# the kayaker's life is represented by a health bar. Hitting rocks or riverbanks will decrease health and picking up fish will raise health.

#inter-session progress
# we will implement a high score feature so that users can keep track of their best games

#Resart from game over
# There will be a play again button that will rerun the game without restarting the program

import pygame
import gamebox
import random
import re
f = open("highscore.txt", "r")
# highscore.txt is a file that keeps track of all scores recorded by a user
history = f.read()
if re.search(r'^\s*$', history):
    initial = '0'
else:
    initial = "\n0"
f.close()
file= open("highscore.txt", "a")
file.write(initial)
file.close()
x = 0

healthbar = [gamebox.from_color(80, 50, "white", 120, 70), gamebox.from_color(80, 50, "green", 107, 60,), gamebox.from_text(83, 50, "HEALTH", 30, "black", 120, 60), gamebox.from_color(10, 50, "dark green", 31, 70), gamebox.from_color(30, 50, "white", 7, 70)]

#building the landscape:
camera = gamebox.Camera(800, 600)
grass = gamebox.from_color(400, 300, "dark green", 800, 600)
bank = [gamebox.from_color(400, 490, "tan", 1000, 28), gamebox.from_color(400, 110, "tan", 800, 28)]
river = gamebox.from_color(400, 300, "blue", 800, 347)
kayaker = gamebox.from_image(100, 300, "Kayak_Character.png")
kayak_core = gamebox.from_image(100, 300, "Kayak_Character2.png")
kayaker.rotate(270)
kayak_core.rotate(270)
kayaker.scale_by(0.13)
kayak_core.scale_by(0.03)
rocks = [gamebox.from_image(700, 300, "rock.png")]
for rock in rocks:
    rock.scale_by(0.04)
rotation_check = 0
right_paddle_turn = -5
left_paddle_turn = 5
stroke_count = 0
ymovement = 3
rock_spawner = 0
fishes = [gamebox.from_color(0, -100, "dark green", 10, 10)]

def game_reset():
    '''
    this function restores all relevant gameboxes and variables to their initial conditions so that the game can be restarted
    :return: none
    '''
    global rocks
    global kayaker
    global kayak_core
    global rotation_check
    global right_paddle_turn
    global left_paddle_turn
    global stroke_count
    global ymovement
    global rock_spawner
    global fishes
    global score_number
    healthbar[1].x = healthbar[0].x
    kayaker = gamebox.from_image(100, 300, "Kayak_Character.png")
    kayak_core = gamebox.from_image(100, 300, "Kayak_Character2.png")
    kayaker.rotate(270)
    kayak_core.rotate(270)
    kayaker.scale_by(0.13)
    kayak_core.scale_by(0.03)
    kayaker.x = healthbar[0].x + 50
    kayaker.y = 300
    kayak_core.x = kayaker.x
    kayak_core.y = 300
    rotation_check = 0
    right_paddle_turn = -5
    left_paddle_turn = 5
    stroke_count = 0
    ymovement = 3
    rock_spawner = 0
    rocks = [gamebox.from_image(700, 300, "rock.png")]
    for rock in rocks:
        rock.scale_by(0.04)
    fishes = [gamebox.from_color(0, -100, "dark green", 10, 10)]
    score_number = 0


def start_screen(keys):
    '''
    this function makes up the starting screen of the game
    :param keys: the user's input
    :return: none
    '''
    global x
    camera.clear('white')
    camera.draw(grass)
    for side in bank:
        camera.draw(side)
    camera.draw(river)
    message = gamebox.from_text(river.x, 200, "RI VER RUN", 90, 'red', italic=True)
    camera.draw(message)
    f = open("highscore.txt", "r")
    previous_scores = f.read().split("\n")
    for score in previous_scores:
        if int(score) > x:
            x = int(score)
    f.close()
    highscore_message = gamebox.from_text(river.x, 275, "HIGHSCORE: " +str(x), 60, 'red')
    button = gamebox.from_color(river.x, 350, "red", 250, 75)
    button_text = gamebox.from_text(river.x, 350, "START", 55, 'white')
    instructions = gamebox.from_text(river.x, 405, "navigate the rocks with the left and right arrow keys", 30, 'red', italic=True)
    instructions2 = gamebox.from_text(river.x, 435, "avoid rocks and riverbanks", 30,'red', italic=True)
    instructions3 = gamebox.from_text(river.x, 465, "collect fish to increase health", 30,'red', italic=True)
    camera.draw(button)
    camera.draw(button_text)
    camera.draw(instructions)
    camera.draw(instructions2)
    camera.draw(instructions3)
    camera.draw(highscore_message)
    camera.display()
    if camera.mouseclick and button.contains(camera.mouse):
        gamebox.timer_loop(30, game)
        gamebox.stop_loop()


score_number = 0
game_pace = 8

def game(keys):
    '''
    this function progresses gameplay
    :param keys: the user's input
    :return: none
    '''
    global rotation_check
    global right_paddle_turn
    global left_paddle_turn
    global ymovement
    global stroke_count
    global rock_spawner
    global score
    global score_number
    global game_pace
    global final
    score = gamebox.from_text(river.x - 220, 50, str(score_number), 65, 'red')
    rock_spawner += 1
    ymovement = game_pace
    camera.x += game_pace
    grass.x += game_pace
    for component in healthbar:
        component.x += game_pace
    score.x += game_pace
    for side in bank:
        side.x += game_pace
    river.x += game_pace

    #kayaker movement:
    if pygame.K_RIGHT in keys:
        if pygame.K_LEFT not in keys:
            stroke_count+= 1
            for side in bank:
                if kayak_core.touches(side):
                    kayak_core.move_to_stop_overlapping(side)
                    kayaker.x = kayak_core.x
                    kayaker.y = kayak_core.y
                    healthbar[1].x -= 1
                    ymovement = 0
            if stroke_count%4 == 0:
                kayaker.flip()
                kayak_core.flip()
            rotation_check += 1
            if rotation_check >= 7:
                rotation_check = 7
                right_paddle_turn = 0
            if rotation_check < 7:
                right_paddle_turn = -5
            kayaker.rotate(right_paddle_turn)
            kayak_core.rotate(right_paddle_turn)
            kayaker.move(8, ymovement)
            kayak_core.move(8, ymovement)
    if pygame.K_LEFT in keys:
        if pygame.K_RIGHT not in keys:
            stroke_count += 1
            for side in bank:
                if kayak_core.touches(side):
                    kayak_core.move_to_stop_overlapping(side)
                    kayaker.x = kayak_core.x
                    kayaker.y = kayak_core.y
                    healthbar[1].x -= 1
                    ymovement = 0
            if stroke_count%4 == 0:
                kayaker.flip()
                kayak_core.flip()
            rotation_check -= 1
            if rotation_check <= -7:
                rotation_check = -7
                left_paddle_turn = 0
            if rotation_check > -7:
                left_paddle_turn = 5
            kayaker.rotate(left_paddle_turn)
            kayak_core.rotate(left_paddle_turn)
            kayaker.move(8, (-1 * ymovement))
            kayak_core.move(8, (-1 * ymovement))
    else:
        if kayak_core.x <= healthbar[0].x -80:
            kayaker.move(4, 0)
            kayak_core.move(4, 0)
        kayaker.move(4, 0)
        kayak_core.move(4, 0)

    #spawning all game characters:
    if rock_spawner % 4 == 0:
        if rock_spawner % 10 == 0:
            score_number += 1
        if random.randint(0, 16) % 15 == 0:
            newrock = gamebox.from_image(700 + (kayak_core.x + 800), random.randint(150, 450), "rock.png")
            newrock.scale_by(0.04)
            rocks.append(newrock)
        if random.randint(0, 16) % 15 == 0:
            newrock = gamebox.from_image(kayak_core.x + 800, random.randint(150, 450), "rock2.png")
            newrock.scale_by(0.02)
            rocks.append(newrock)
        if random.randint(0, 501) % 500 == 0:
            fish = gamebox.from_image(kayak_core.x + 800, random.randint(150, 450), "fish.png")
            fish.scale_by(0.1)
            fishes.append(fish)

    #collision detection:
    for rock in rocks:
        if kayak_core.touches(rock):
            kayak_core.move_to_stop_overlapping(rock)
            kayaker.x = kayak_core.x
            kayaker.y = kayak_core.y
            healthbar[1].x -= 2
        if rock.x < (healthbar[0].x - 70):
            del rock

    for fish in fishes:
        if kayak_core.touches(fish):
            fish.y = 1000
            if healthbar[1].x <= healthbar[0].x- 25:
                healthbar[1].x += 25
            elif healthbar[1].x < healthbar[0].x:
                healthbar[1].x = healthbar[0].x
        if fish.x < (healthbar[0].x - 70):
            del fish

    camera.draw(grass)
    for side in bank:
        camera.draw(side)
    camera.draw(river)
    for rock in rocks:
        camera.draw(rock)
    for fish in fishes:
        camera.draw(fish)
    camera.draw(kayaker)
    camera.draw(score)
    camera.draw(kayak_core)
    for component in healthbar:
        camera.draw(component)
    #calls end screen when game is over
    if healthbar[1].x <= healthbar[0].x - 101:
        final = score_number
        with open("highscore.txt", "a") as f:
            f.write("\n" + str(final))
        game_reset()
        gamebox.timer_loop(30, end_screen)
        gamebox.stop_loop()
    camera.display()


def end_screen(keys):
    '''
    this function makes up the ending screen of the game
    :param keys: the user's input
    :return: none
    '''
    camera.clear('white')
    camera.draw(grass)
    for side in bank:
        camera.draw(side)
    camera.draw(river)
    final_score = gamebox.from_text(river.x, 220, "SCORE: "+str(final), 80, 'red')
    playagain = gamebox.from_color(river.x, 420, "red", 250, 75)
    playagain_text = gamebox.from_text(river.x, 420, "PLAY AGAIN", 55, 'white')
    camera.draw(playagain)
    camera.draw(playagain_text)
    quit = gamebox.from_color(river.x, 320, "red", 250, 75)
    quit_text = gamebox.from_text(river.x, 320, "QUIT", 55, 'white')
    camera.draw(final_score)
    camera.draw(quit)
    camera.draw(quit_text)
    camera.display()
    if camera.mouseclick and quit.contains(camera.mouse):
        gamebox.stop_loop()
    if camera.mouseclick and playagain.contains(camera.mouse):
        gamebox.timer_loop(30, start_screen)
        gamebox.stop_loop()

#the starting screen is looped, which will call the game function, which will call the starting screen again
gamebox.timer_loop(30, start_screen)