import pew_tunnel as pew
import random
import pygame
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
import numpy as np

#########################################################################
#FUNCTIONS
#########################################################################


simulator = Aer.get_backend('statevector_simulator')

def qrand(nbits):
    """generates nbits real random numbers using quantum state measurements in qiskit."""

    circ = QuantumCircuit(1, 1)
    circ.h(0)
    circ.measure(0, 0)
    val = np.zeros(nbits)
    for i in range(nbits):
        job=execute(circ, simulator)
        res = job.result()
        vec = res.get_statevector()
        val[i] = vec[0] * 1 + vec[1] * 0
    #convert val array into bitstring b and then into integer
    b = ''
    for i in range(nbits):
        b += str(int(val[i]))

    integ= int(b, 2)
    return integ

def Pt(U0, E, L, betac, gamma_sqc):
    """return tunneling probability for square barrier"""
    return 1/ (np.cosh(betac * L)**2 + gamma_sqc * np.sinh(betac * L)**2)

def beta(U0, E):
    """supply function for Pt"""
    return np.sqrt(2* (U0 - E))

def gamma_sq(U0, E):
    """supply function for Pt"""
    return 0.25 * ((1 - E/U0)/(E/U0) + (E/U0)/(1-E/U0) - 2)

def theta(p_tunnel):
    """returns rotation angle corresponding to tunneling prob. p_tunnel"""
    return 2 * np.arcsin(np.sqrt(p_tunnel))

def tunnelres(U0, length_snake, L, betac, gamma_sqc):
    """returns 0 if tunnel, returns 1 if no tunnel"""
    P_t = Pt(U0, length_snake, L, betac, gamma_sqc) #get tunneling prob depending on current snake length
    theta_rot = theta(P_t) #get rot angle

    #qcirc
    qr = QuantumRegister(1)
    cr  = ClassicalRegister(1)
    circ = QuantumCircuit(qr, cr)
    circ.rx(theta_rot, qr[0])
    circ.measure(qr, cr)
    job = execute(circ, simulator)
    res = job.result()
    vec = res.get_statevector()
    val = vec[0] * 1 + vec[1] * 0
    if val == 1:
        return 0
    else:
        return 1
    #r= random.randint(0, 1)
    #return round(r)

def Qand(First_bool,Second_bool):

    a = int(First_bool)
    b = int(Second_bool)

    q = QuantumRegister(3)

    qc = QuantumCircuit(q)
    if a is 1:
        qc.x(0)
    if b is 1:
        qc.x(1)
    qc.ccx(q[0], q[1], q[2])
    qc.draw()

    backend = Aer.get_backend('statevector_simulator')
    job = execute(qc, backend)
    result = job.result()
    outputstate = result.get_statevector(qc, decimals=8)
    Q_and = bool(int(np.real(outputstate[7])))
    
    return Q_and

def Qor(First_bool,Second_bool):

    a = int(First_bool)
    b = int(Second_bool)

    q = QuantumRegister(3)

    qc = QuantumCircuit(q)
    if a is 1:
        qc.x(0)
    if b is 1:
        qc.x(1)
    qc.ccx(q[0], q[1], q[2])
    qc.draw()

    backend = Aer.get_backend('statevector_simulator')

    job = execute(qc, backend)

    result = job.result()

    outputstate = result.get_statevector(qc, decimals=8)

    if a is 1 and b is 0:
        Q_or = bool(int(np.real(outputstate[1])))
    elif a is 0 and b is 1:
        Q_or = bool(int(np.real(outputstate[2])))
    else:
        Q_or = bool(int(np.real(outputstate[7])))
    
    return(Q_or)



##########################################################################
#MAIN
##########################################################################




#initialize pew
dis = pew.init()
screen = pew.Pix()
#set size
bits = 3
ds= 2**bits #displazsize

#set game starting parameters
game_speed = 4
snake = [(2, 4)]
dx, dy = 1, 0
apple_x, apple_y = 6, 4
screen.pixel(apple_x, apple_y, 2)
howmanyapples = 1 #marker for total number of eaten apples, used for scoring


#set graphics for probability display
pygame.font.init()
#gate backkgorund
font1 = pygame.font.Font(None, 33)
text = font1.render('Probability for tunneling is', True, (255, 0, 0))
dis.blit(text, (20, 330))
font2 = pygame.font.Font(None, 45)
text2 = font2.render('100%', True, (255, 0, 0))
dis.blit(text2, (130, 360))
ima = pygame.image.load('pewblack.jpg')



#tunneling parameters
U0=37 #max snake length = 6x6 = 36
E=1
L=0.05 #optimal barrier size for nice tunneling probabilities

#initialize tunneling tracker
tunnel=0 #don't see other side as second barrier
snakepos=1 #marker of snakepos, 1=head, increase towards tail
headtunnel=0 #let the head tunnel again through other even if tail still in process


while True: #snake runs
    #create barrier
    bar= []
    for i in range(ds):
        screen.pixel(0, i, 1)
        screen.pixel(ds-1, i, 1)
        screen.pixel(i, 0, 1)
        screen.pixel(i, ds-1, 1)
        bar.append((0, i))
        bar.append((ds-1, i))
        bar.append((i, 0))
        bar.append((i, ds-1))

    #find the head
    if len(snake) > 1:
        x, y = snake[-2]
        screen.pixel(x, y, 1)
    x, y = snake[-1]
    screen.pixel(x, y, 3) #color the head yellow

    pew.show(screen)
    pew.tick(1 / game_speed)

    #get commands
    keys = pew.keys()
    if headtunnel==0:
        if  Qand(bool(int(keys & pew.K_UP)),dy == 0) is True:
            dx, dy = 0, -1
            #print(bool(int(keys & pew.K_UP)))
            #print(dy == 0)
            #print(Qand(bool(int(keys & pew.K_UP)),dy == 0))
        elif Qand(bool(int(keys & pew.K_LEFT)),dx == 0) is True:
            #print(str(keys & pew.K_LEFT) + 'right')
            dx, dy = -1, 0
        elif Qand(bool(int(keys & pew.K_RIGHT)),dx == 0) is True:
            #print(str(keys & pew.K_RIGHT) + 'right')
            dx, dy = 1, 0
        elif Qand(bool(int(keys & pew.K_DOWN)),dy == 0) is True:
            #print(str(keys & pew.K_DOWN) + 'down')
            dx, dy = 0, 1
        x = (x + dx) % 8
        y = (y + dy) % 8
    elif headtunnel==1: #steering not allowed during tunneling of the head (during two rounds)
        x = (x + dx) % 8
        y = (y + dy) % 8
        headtunnel=2
    elif headtunnel>=2:
        x = (x + dx) % 8
        y = (y + dy) % 8
        headtunnel=0


    ##TUNNELING PROCESS
    #snake tail tunnels
    if Qand(tunnel>0,snakepos<=len(snake)) is True:
        #get segment for tunneling
        sx, sy = snake[-snakepos]
        E=len(snake)/2 #divide by two for lower tunnel prob for tail (lower mass->lower energy)
        tunnels = tunnelres(U0, E, L, beta(U0, E), gamma_sq(U0, E))
        if tunnels==1: #tunnels
            snakepos+=1
        else: #does not tunnel
            del snake[-snakepos]
            screen.pixel(sx, sy, 0)

    #reset if last segment tunneled
    if Qand(tunnel>0, snakepos==(len(snake)+1)) is True:
        tunnel=0
        snakepos=1

    #snake head tunnels
    if Qand(headtunnel==0, (x, y) in bar) is True:
        E=len(snake)
        tunnel = tunnelres(U0, E, L, beta(U0, E), gamma_sq(U0, E))
        if Qand(tunnel==0, len(snake) != 1) is True: #head doesn't tunnel --> game over
            break
        else:
            snakepos+=1
            headtunnel+=1
    elif Qand(headtunnel==1, (x, y) in bar) is True:
        headtunnel=0

    #display tunneling prob.
    E = len(snake)
    if E > 1:
        prob = Pt(U0, E, L, beta(U0, E), gamma_sq(U0, E))
        text3 = font2.render(str(int(round(prob * 100))) + '%', True, (255, 0, 0))
        dis.blit(ima, (130, 360))
        dis.blit(text3, (130, 360))
    else: #if length of snake ==1 (only head), tunneling prob = 100%
        dis.blit(ima, (130, 360)) #cover the ultimate prob. display
        dis.blit(text2, (130, 360)) #text2 = '100%'
    #####TUNNEL END


    if (x, y) in snake:     #exit, game over condition
        break

    snake.append((x, y))

    #apple generation
    if Qand(x == apple_x, y == apple_y) is True:
        screen.pixel(apple_x, apple_y, 0)
        apple_x, apple_y = snake[0]
        while Qor((apple_x, apple_y) in snake, (apple_x, apple_y) in bar) is True:
            apple_x = qrand(bits)              #random.getrandbits(3) #use this for pseudo random number gen, no qiskit needed
            apple_y = qrand(bits)              #random.getrandbits(3)
        screen.pixel(apple_x, apple_y, 2)
        game_speed += 0.2 #increase game speed
        howmanyapples += 1 #increase number of eaten apples, score +1
    else:
        x, y = snake.pop(0)
        screen.pixel(x, y, 0)


text = pew.Pix.from_text("Game over!") #Game over message and closing
for dx in range(-8, text.width):
    screen.blit(text, -dx, 1)
    pew.show(screen)
    pew.tick(1 / 12)

text = pew.Pix.from_text("Score:" + str(int(howmanyapples))) #Score message
for dx in range(-8, text.width):
    screen.blit(text, -dx, 1)
    pew.show(screen)
    pew.tick(1 / 12)

pygame.quit()