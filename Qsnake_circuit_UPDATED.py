import pew_circuit as pew
from qiskit import QuantumCircuit, execute, Aer
#from aether import QuantumCircuit, simulate
import pygame
import numpy as np

simulator = Aer.get_backend('qasm_simulator')
shot=1

def Qand(First_bool,Second_bool):
    First_bool=bool(First_bool)
    Second_bool=bool(Second_bool)    
    a = int(First_bool)
    b = int(Second_bool)
    qc = QuantumCircuit(3,1)
    if a == 1:
        qc.x(0)
    if b == 1:
        qc.x(1)
    qc.ccx(0, 1, 2) #toffoli
    qc.measure(2,0)    
    job = execute(qc, simulator,shots=shot)
    counts = job.result().get_counts()
    state = [key  for (key, value) in counts.items() if value ==1]
    return bool(int(state[0]))

def Qnand(First_bool,Second_bool):
    First_bool=bool(First_bool)
    Second_bool=bool(Second_bool)    
    a = int(First_bool)
    b = int(Second_bool)
    qc = QuantumCircuit(3,1)
    if a == 1:
        qc.x(0)
    if b == 1:
        qc.x(1)
    qc.ccx(0, 1, 2) #toffoli
    qc.x(2)
    qc.measure(2,0)    
    job = execute(qc, simulator,shots=shot)
    counts = job.result().get_counts()
    state = [key  for (key, value) in counts.items() if value ==1]
    return bool(int(state[0]))

def Qor(First_bool,Second_bool):
    return Qnand(Qnand(First_bool,First_bool),Qnand(Second_bool,Second_bool))

def qrand(nbits):
    """generates nbits real random numbers using quantum state measurements in qiskit."""
    circ = QuantumCircuit(1, 1)
    circ.h(0)
    circ.measure(0, 0)
    b=''#string holder
    for i in range(nbits):
        job=execute(circ, simulator,shots=shot)
        counts = job.result().get_counts()
        state = [key  for (key, value) in counts.items() if value == 1] #find the measured state, this is a list
        b=b+state[0] #state[0] is a string
    return int(b, 2)

dis = pew.init()
screen = pew.Pix()
#Selecting game speed
init_speed =3
game_speed = init_speed 
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
corr = [0, 1, 0, 2] #correct sequence of gates
images = {}
for i in range(4):
    imag_ = pygame.image.load(str(i+1) + 'c.png')
    x_size = int((i+1)*65)
    images[i] = imag_#pygame.transform.scale(imag_,(x_size,85))

g=0 #tracks selected gate
currg=0 #tracks current position in circuit
success=False #tracks whether or not circuit is successfully constructed
ima3 = pygame.image.load('1c.png')
#ima3 = pygame.transform.scale(ima3,(65,50))
dis.blit(ima3, (45, 325))
#Selecting initial position of the snake
snake = [(3,3)]
#Selecting initial velocity of the snake
dx, dy = 1, 0
#Selecting initial position of the apple
apple_x, apple_y = 6, 4
screen.pixel(apple_x, apple_y, 1)
#Selecting the initial position of the first noise
nx=3
ny=4
noise=[(nx, ny)]
while True:
    screen.pixel(noise[0][0],  noise[0][1],2)
    #Here we print the head of the snake
    if len(snake) > 1:
        x, y = snake[-2]
        screen.pixel(x, y, 1)
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
    
    #Gate switch
    if keys & pew.K_O:
        pygame.draw.rect(dis,(255,255,255),(0,320,50,50))
        g = (g+1) % 3 #cycle between gates
        font1 = pygame.font.Font(None, 70)
        text = font1.render(gates[g], True, (255, 0, 0))
        dis.blit(text, (10, 330))

    #Now are going to update the position of the head of the snake
    #We define the next position of the head depending on the velocity
    x = (x + dx) %8
    y = (y + dy) %8

    #Now we define a loop to end the loop (and the game) if the next position
    # of the head is in the snake or it goes out of the grid
    if Qor((x, y) in snake, (x,y) in noise):
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
    if Qand(x == apple_x, y == apple_y):
        if g != corr[currg]:
            break
        else:
            if currg == len(corr)-1: #if the required sequence is accomplished
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
        screen.pixel(apple_x, apple_y, 1)
#        k=k+1
        nx=snake[0][0]
        ny=snake[0][1]
        while Qor(Qor(Qor((nx,ny) in snake, (Qand(nx==apple_x, ny==apple_y))) ,(nx,ny) in noise) , (nx,ny)==(x,y)):
            nx=qrand(3) #as opposed to random.getrandbits(3)
            ny=qrand(3)
        noise.append((nx,ny))
        screen.pixel(nx, ny,2)
        #We increase the speed of the game
        game_speed += 0.2
    #If the snake eats the apple we don't delete the last pixel of the snake. Otherwise we remove
    # the last pixel to not increase the size of the snake
    else:
        x, y = snake.pop(0)
        screen.pixel(x, y, 0)

def blit_screen(screen,text):
    for dx in range(-8, text.width):
        screen.blit(text, -dx, 1)
        pew.show(screen)
        pew.tick(1 / 12)

#When the loop is finished we print the game over screen
#turn off all pixels
if success == True:
    text = pew.Pix.from_text("You win!")
    for dx in range(-8, text.width):
        screen.blit(text, -dx, 1)
        pew.show(screen)
        pew.tick(1 / 12)
        
else:
    text = pew.Pix.from_text("Game over!")
    blit_screen(screen,text)
    for dx in range(-8, text.width):
        screen.blit(text, -dx, 1)
        pew.show(screen)
        pew.tick(1 / 12)
pygame.quit()