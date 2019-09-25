
import pew_circuit as pew
import random
from aether import QuantumCircuit, simulate
import pygame
import numpy as np

def qrand(nbits):
    # generates nbits real random numbers using quantum state measurements in qiskit.
    circ = QuantumCircuit(1, 1)
    circ.h(0)
    circ.measure(0, 0)
    val = simulate(circ, shots=nbits, get='memory')
    b = ''
    for i in range(nbits):

        b += str(val[0])

    integ= int(b, 2)
    return integ

dis = pew.init()
screen = pew.Pix()
#Selecting game speed
init_speed =1 
game_speed = init_speed 
k=0
#circuit graphics
pygame.font.init()
#add backgorund
pygame.draw.rect(dis,(255,255,255),(0,320,320,100))
#gate backkgorund
#add gate, change from H to Z to Meas by key stroke
font1 = pygame.font.Font(None, 70)
text = font1.render('H', True, (255, 0, 0))
dis.blit(text, (10, 330))
g=0

#add gate, change from H to Z to Meas by key stroke
gates = np.zeros(3, dtype=str)
gates[0] = 'H'
gates[1] = 'Z'
gates[2] = 'M'
corr = [0, 1, 0, 2]
images = {}
for i in range(4):
    imag_ = pygame.image.load(str(i+1) + 'c.png')
    x_size = int((i+1)*65)
    images[i] = imag_#pygame.transform.scale(imag_,(x_size,85))

def one_round(speed):
    g=0
    currg=0
    success=False
    ima3 = pygame.image.load('1c.png')
    #ima3 = pygame.transform.scale(ima3,(65,50))
    dis.blit(ima3, (45, 325))
    #Selecting initial position of the snake
    snake = [(3,3)]
    #Selecting initial velocity of the snake
    dx, dy = 1, 0
    #Selecting initial position of the apple
    apple_x, apple_y = 6, 4
    screen.pixel(apple_x, apple_y, 2)
    #Selecting the initial position of the first noise
    nx=random.getrandbits(3)
    ny=random.getrandbits(3)
    noise=[(nx, ny)]
    while True:
        screen.pixel(noise[0][0],  noise[0][1],1)
        ##Now let's implement a loop for the game
        # Here we are going to print the snake
        #Here we print the head of the snake
        x, y = snake[-1]
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1 / game_speed)

        #Here we change the velocity of the snake depending on the key input
        keys = pew.keys()
        if keys & pew.K_UP and dy == 0:
            dx, dy = 0, -1

        elif keys & pew.K_LEFT and dx == 0:
            dx, dy = -1, 0

        elif keys & pew.K_RIGHT and dx == 0:
            dx, dy = 1, 0

        elif keys & pew.K_DOWN and dy == 0:
            dx, dy = 0, 1
        #gate switch
        if keys & pew.K_O:
            pygame.draw.rect(dis,(255,255,255),(0,320,50,50))
            g = (g+1) % 3
            font1 = pygame.font.Font(None, 70)
            text = font1.render(gates[g], True, (255, 0, 0))
            dis.blit(text, (10, 330))

        #Now are going to update the position of the head (and the snake)
        #We define the next position of the head depending on the velocity
        x = (x + dx)
        y = (y + dy)

        #Now we define a loop to end the loop (and the game) if the next position
        # of the head is in the snake or it goes out of the grid
        if (x, y) in snake or x==9 or y==9 or x==-1 or y==-1 or (x,y) in noise:
            #Here we turn of all the pixles from the snake and the apple
            for (i,j) in snake:
                screen.pixel(i,j,0)
            screen.pixel(apple_x,apple_y,0)
            for (i,j) in noise:
                screen.pixel(i,j,0)
            break
        #If none of those thing happens the head of the snake gets updated to the new position
        snake.append((x, y))

        #Now we create a conditional loop for changing the size and spawning new apples depending
        # on if the snake eats the apple or not
        if x == apple_x and y == apple_y:
            if g != corr[currg]:
                break
            else:
                if currg == 3:
                    success=True
                    break
                dis.blit(images[currg+1], (45, 325))
                currg+=1

            #If the snake eats the apple we turn of the pixel of the apple
            screen.pixel(apple_x, apple_y, 0)
            #Now we define the coordinates of the apple to lie inside the snake for the loop
            apple_x, apple_y = snake[0]
            #We create a loop to generate an apple ouside the snake
            while (apple_x, apple_y) in snake or (apple_x, apple_y) in noise:
                apple_x=qrand(3)
                apple_y=qrand(3)
            #We light the pixels of the new apple
            screen.pixel(apple_x, apple_y, 2)
            k=k+1
            nx=snake[0][0]
            ny=snake[0][1]
            while (nx,ny) in snake or (nx==apple_x and ny==apple_y) or (nx,ny) in noise or (nx,ny)==(x,y):
                nx=random.getrandbits(3)
                ny=random.getrandbits(3)
            noise.append((nx,ny))
            screen.pixel(nx, ny,1)
            #We increase the speed of the game
            game_speed += 0.2
        #If the snake eats the apple we don't delete the last pixel of the snake. Otherwise we remove
        # the last pixel to not increase the size of the snake
        else:

            x, y = snake.pop(0)

            screen.pixel(x, y, 0)
    return success

def blit_screen(screen,text):
    for dx in range(-8, text.width):
        screen.blit(text, -dx, 1)
        pew.show(screen)
        pew.tick(1 / 12)

success = one_round(game_speed)
#When the loop is finished we print the game over screen
if success is True:
    for (i,j) in snake:
            screen.pixel(i,j,0)
    screen.pixel(apple_x,apple_y,0)
    for (i,j) in noise:
        screen.pixel(i,j,0)
    game_speed += 1

    if game_speed >5:
        text = pew.Pix.from_text("You win!")
        blit_screen(screen,text)
    else:
        text = pew.Pix.from_text("Level "+str(game_speed-init_speed))
        blit_screen(screen,text)
        one_round(game_speed)

else:
    text = pew.Pix.from_text("Game over! Level " +str(game_speed-init_speed-1))
    blit_screen(screen,text)
