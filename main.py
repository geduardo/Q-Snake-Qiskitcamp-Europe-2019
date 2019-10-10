import sys
import os
import time
import pew
import pew
import random
from aether import QuantumCircuit, simulate
def qrand(nbits):
    circ = QuantumCircuit(1, 1)
    circ.h(0)
    circ.measure(0, 0)
    val = simulate(circ, shots=nbits, get='memory')
    b = ''
    for i in range(nbits):
        b += str(val[i])
    integ = int(b, 2)
    return integ
pew.init()
screen = pew.Pix()
l=True
while True:
    if l:
        gm_sp = 5
        pts=0
        snake = [(3,3)]
        dx, dy = 1, 0
        apple_x, apple_y = 6, 6
        screen.pixel(apple_x, apple_y, 3)
        l=False
        
    while True:
        x, y = snake[-1]
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1 / gm_sp)
        keys = pew.keys()
        if keys & pew.K_UP and dy == 0:
            dx, dy = 0, -1
        elif keys & pew.K_LEFT and dx == 0:
            dx, dy = -1, 0
        elif keys & pew.K_RIGHT and dx == 0:
            dx, dy = 1, 0
        elif keys & pew.K_DOWN and dy == 0:
            dx, dy = 0, 1
    
        x = (x + dx)
        y = (y + dy)

        s_b=3
        y_pos_b=4
        x_pos_b=4
        barrier=[(x_pos_b,y_pos_b)]

        for i in range(0,s_b):
            barrier.append(((x_pos_b+i),y_pos_b))
            screen.pixel(x_pos_b+i,y_pos_b,1)

        if (x, y) in snake or x ==9 or y == 9 or x == -1 or y == -1:
            for (i,j) in snake:
                screen.pixel(i,j,0)
            screen.pixel(apple_x,apple_y,0)
            break

        if (x, y) in barrier and qrand(3)<3:
            for (i,j) in snake:
                screen.pixel(i,j,0)
            screen.pixel(apple_x,apple_y,0)
            break
        snake.append((x, y))
        if x == apple_x and y == apple_y:
            screen.pixel(apple_x, apple_y, 0)
            apple_x, apple_y = snake[0]
            while (apple_x, apple_y) in snake or (apple_x, apple_y) in barrier:
                apple_x=qrand(3)
                apple_y=qrand(3)
            screen.pixel(apple_x, apple_y, 2)
            gm_sp += 0.2
            pts=pts+1
        else:
            x, y = snake.pop(0)
            screen.pixel(x, y, 0)
    text = pew.Pix.from_text('Points: ' + str(pts))
    l=True
    for dx in range(-8, text.width):
        screen.blit(text, -dx, 1)
        pew.show(screen)
        pew.tick(1 / 12) 
    text = pew.Pix.from_text("Game over!")

    for dx in range(-8, text.width):
        screen.blit(text, -dx, 1)
        pew.show(screen)
        pew.tick(1 / 12) 
