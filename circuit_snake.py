import pew
import random
import numpy as np


##def create_snake():
##    size = snake_size*3*snake_size
##    snake = np.zeros((2, size)) 
##    snake_x = 16 
##    snake_y = 25
##    i=0
##    for val in itertools.product(range(snake_size),range(snake_size*3))
##        snake[0,i] = val[1] 
##        snake[1,i] = val[0] 
##return snake
pew.init()
screen = pew.Pix()




def print_snake(x,y,size,horizontal=False,remove=False):
    if remove is False:
        color =2
    else:
        color = 0
    if horizontal is True:
        for i in range(size):
            screen.pixel(x+i,y,color)
            screen.pixel(x-i,y,color)
    else: 
        for i in range(size):
            screen.pixel(x,y-i,color)
            screen.pixel(x,y+i,color)

def plot_full_box(x,y,width,height):
    for i in range(x, x+width):
        for j in range(y, y+height):
            screen.pixel(i,j,2)

def plot_box(x,y,width,height):
    for i in range(x, x+width):
        for j in [y, y+height]:
            screen.pixel(i,j,1)
    for i in [x, x+width]:
        for j in range(y, y+height):
            screen.pixel(i,j,1)

def empty_box(x,y,width=4,height=6):
    for i in range(x, x+width):
        for j in [y, y+height]:
            screen.pixel(i,j,0)
    for i in [x, x+width]:
        for j in range(y, y+height):
            screen.pixel(i,j,0)

def print_gate(gate,apple_x,apple_y):
    text = pew.Pix.from_text(gate,color=2,bgcolor=1)
    screen.blit(text,apple_x,apple_y)
    width= text.width
    height = text.height
    plot_box(x=apple_x-1,y=apple_y-1,width=width,height=height)
    return width, height

def return_gates(gate_ind,apple_x,apple_y):
    list_gates = ["Z","H","Y"]
    gate_ind = (gate_ind+1)%len(list_gates) 
    gate = list_gates[gate_ind] 
    width,height = print_gate(gate,apple_x,apple_y)
    return gate,width,height,gate_ind

def remove_gate(apple_x,apple_y):
    text = pew.Pix.from_text("H",color=0,bgcolor=0)
    screen.blit(text,apple_x,apple_y)
    empty_box(apple_x-1,apple_y-1)
def main():
    res = 340,340
    screen_size = int(res[0]/20),int(res[1]/20) 

    game_speed = 6 
    dx, dy = 1, 0
    snake = [(16, 20)]
    apple_x, apple_y = 5,6#int(screen_size[0]/2), int(screen_size[1]/2)
    gate,width,height,ind= return_gates(0,apple_x,apple_y)
    screen.pixel(apple_x, apple_y, 2)


    required_list = ["H","Z","H"]
    required_ind = 0

    success = False
    first=True
    horizontal=True

    while True:
        #Plot full snake if first iteration
        x, y = snake[-1]
        screen.pixel(x, y, 3)
        
       # if (x, y) in snake:
       #     break


        pew.show(screen)
        pew.tick(1 / game_speed)

        keys = pew.keys()
        if keys & pew.K_UP and dy == 0:
            dx, dy = 0, -1
        elif keys & pew.K_LEFT and dx == 0:
            dx, dy = -1, 0
        elif keys & pew.K_RIGHT and dx == 0:
            dx, dy = 1, 0
        elif keys & pew.K_DOWN and dy == 0:
            dx, dy = 0, 1
        x = (x + dx) % screen_size[0] 
        y = (y + dy) % screen_size[1]
        snake.append((x, y))
        if keys & pew.K_O:
            remove_gate(apple_x,apple_y)
            gate,width,height,ind= return_gates(ind,apple_x,apple_y)
            #screen.pixel(apple_x, apple_y, 1)


        if x >= apple_x-1 and x<apple_x+width  and y >= apple_y -1 and y<apple_y+height:
            #screen.pixel(apple_x, apple_y, 0)
            remove_gate(apple_x,apple_y)
            #Ate right gate
            if required_list[required_ind] == gate:
                print("Ate " + gate)
                #screen.pixel(apple_x, apple_y, 0)
                required_ind +=1
                if required_ind == len(required_list):
                    success = True
                    break

            else:
                break
            while True: 
                check_snake_list = np.zeros(len(snake),dtype=bool)
            #while (apple_x, apple_y) in snake:
                apple_x = random.randint(2,int(screen_size[0]-width-2))
                apple_y = random.randint(2,int(screen_size[1]-height-2))
                for i,element in enumerate(snake):
                    if element[0] >= apple_x-3 and element[0] < apple_x + width+2 and element[1] >= apple_y-3  and element[1] < apple_y + height+2:
                        check_snake_list[i] = False 
                    else:
                        check_snake_list[i] = True 
                if np.all(check_snake_list) == True:
                    break 
            gate,width,height,ind= return_gates(ind,apple_x,apple_y)
            #screen.pixel(apple_x, apple_y, 2)
            #game_speed += 0.2
        else:
        #print_snake(x,y,2,horizontal=horizontal,remove=True)
            x, y = snake.pop(0)
            screen.pixel(x, y, 0)
        #screen.pixel(x, y, 0)


    if success is False:
        text = pew.Pix.from_text("Game over!")
    else:
        text = pew.Pix.from_text("You win!")
    for dx in range(-screen_size[0], text.width):
        screen.blit(text, -dx, int(screen_size[1]/2))
        pew.show(screen)
        pew.tick(1 / 12)

main()
