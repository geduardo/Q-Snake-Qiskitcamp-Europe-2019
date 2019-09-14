import pew
import random
from aether import QuantumCircuit, simulate
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

pew.init()
screen = pew.Pix()
#Selecting game speed
game_speed = 5
k=0
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
m=0
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
        m=m+1
        if m>3:
            break
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

#When the loop is finished we print the game over screen
if m>3:
    for (i,j) in snake:
            screen.pixel(i,j,0)
    screen.pixel(apple_x,apple_y,0)
    for (i,j) in noise:
        screen.pixel(i,j,0)
    text = pew.Pix.from_text("You win!")

    for dx in range(-8, text.width):

        screen.blit(text, -dx, 1)

        pew.show(screen)
        
        pew.tick(1 / 12)
    
else:
    text = pew.Pix.from_text("Game over!")

    for dx in range(-8, text.width):

        screen.blit(text, -dx, 1)

        pew.show(screen)

        pew.tick(1 / 12)