import pew
import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
import numpy as np

#########################################################################
#FUNCTIONS
#########################################################################

simulator = Aer.get_backend('statevector_simulator')

def qrand(nbits):
    "generates nbits real random numbers using quantum state measurements in qiskit."

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
    return 1/ (np.cosh(betac * L)**2 + gamma_sqc * np.sinh(betac * L)**2)

def beta(U0, E):
    return np.sqrt(2* (U0 - E))

def gamma_sq(U0, E):
    return 0.25 * ((1 - E/U0)/(E/U0) + (E/U0)/(1-E/U0) - 2)

def theta(p_tunnel):
    return 2 * np.arcsin(np.sqrt(p_tunnel))

def tunnelres(U0, length_snake, L, betac, gamma_sqc):
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
    print(P_t, theta_rot/(2*np.pi)*360)
    if val == 1:
        return 0
    else:
        return 1
    #r= random.randint(0, 1)
    #return round(r)




##########################################################################
#MAIN
##########################################################################




#initialize pew
pew.init()
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


#tunneling parameters
U0=37 #max snake length =36
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
        if keys & pew.K_UP and dy == 0:
            dx, dy = 0, -1
        elif keys & pew.K_LEFT and dx == 0:
            dx, dy = -1, 0
        elif keys & pew.K_RIGHT and dx == 0:
            dx, dy = 1, 0
        elif keys & pew.K_DOWN and dy == 0:
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
    if tunnel>0 and snakepos<=len(snake):
        #get segment for tunneling
        sx, sy = snake[-snakepos]
        E=len(snake)/2 #divide by two for lower tunnel prob for tail (lower mass->lower energy)
        tunnels = tunnelres(U0, E, L, beta(U0, E), gamma_sq(U0, E))
        print('segment', snakepos, 'tunnels?', tunnels)
        if tunnels==1: #tunnels
            snakepos+=1
        else: #does not tunnel
            print(snakepos, "does not tunnel")
            del snake[-snakepos]
            screen.pixel(sx, sy, 0)

    #reset if last segment tunneled
    if tunnel>0 and snakepos==(len(snake)+1):
        tunnel=0
        snakepos=1

    #snake head tunnels
    if headtunnel==0 and (x, y) in bar:
        E=len(snake)
        tunnel = tunnelres(U0, E, L, beta(U0, E), gamma_sq(U0, E))
        print('head tunnels?', tunnel)
        if tunnel==0 and len(snake) != 1: #head doesn't tunnel --> game over
            break
        else:
            print('head tunnels')
            snakepos+=1
            headtunnel+=1
    elif headtunnel==1 and (x, y) in bar:
        headtunnel=0
    #####TUNNEL END


    if (x, y) in snake:     #exit, game over condition
        break

    snake.append((x, y))

    #apple generation
    if x == apple_x and y == apple_y:
        screen.pixel(apple_x, apple_y, 0)
        apple_x, apple_y = snake[0]
        while (apple_x, apple_y) in snake or (apple_x, apple_y) in bar:
            apple_x = qrand(bits)              #random.getrandbits(3) #use this for pseudo random number gen, no qiskit needed
            apple_y = qrand(bits)              #random.getrandbits(3)
        screen.pixel(apple_x, apple_y, 2)
        game_speed += 0.2
    else:
        x, y = snake.pop(0)
        screen.pixel(x, y, 0)


text = pew.Pix.from_text("Game over!") #Game over message and closing
for dx in range(-8, text.width):
    screen.blit(text, -dx, 1)
    pew.show(screen)
    pew.tick(1 / 12)

text = pew.Pix.from_text("Score:" + str(len(snake))) #Score message
for dx in range(-8, text.width):
    screen.blit(text, -dx, 1)
    pew.show(screen)
    pew.tick(1 / 12)
