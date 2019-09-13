import pew
import random
import numpy

pew.init()
screen = pew.Pix()

game_speed = 4
snake_size = 4

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

snake = [16, 20]
dx, dy = 1, 0

res = 1360,680
screen_size = int(res[0]/20),int(res[1]/20) 


def remove_col(x,y,width,height,dx,dy):
    #0,1
    if dy==0:
        col = y
        if dx == 1:
            row= x-width+1
        elif dx == -1:
            row = x+width-1
    #0,-1
    elif dx == 0:
        row  = x
        if dy ==1:
            col = y-height
        elif dy== -1:
            col = y+height
    for i in range(width):
        screen.pixel(x+i,col,0)


def add_col(x,y,width,height,dx,dy):
    #0,1
    for i in range(width):
        screen.pixel(x+i,y,2)

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


def print_gate(gate,apple_x,apple_y):
    text = pew.Pix.from_text(gate[:2],color=2,bgcolor=1)
    screen.blit(text,apple_x,apple_y)
    width= text.width
    height = text.height
    plot_box(x=apple_x-1,y=apple_y-1,width=width,height=height)
    return width, height

def return_gates():
    list_gates = ["H","CNOT","Me","CX","CZ"]
    gate_ind = random.randint(0,len(list_gates)-1)
    gate = list_gates[gate_ind] 
    width,height = print_gate(gate,apple_x,apple_y)
    return gate,width,height

apple_x, apple_y = 5,6#int(screen_size[0]/2), int(screen_size[1]/2)
gate,width,height= return_gates()
screen.pixel(apple_x, apple_y, 2)


required_list = ["H","CNOT","CNOT","H","Me","CX","CZ"]
required_ind = 0

success = False
first=True

while True:
    #Plot full snake if first iteration
    x, y = snake
    screen.pixel(x, y, 3)

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
    snake = x,y
    if keys & pew.K_O:
        gate,width,height= return_gates()
        #screen.pixel(apple_x, apple_y, 1)

    #if (x, y) in snake:
    #    break

    if x >= apple_x-1 and x<=apple_x+width  and y >= apple_y -1 and y<=apple_y+height:
        #screen.pixel(apple_x, apple_y, 0)
        apple_x, apple_y = snake[0]
        #Ate right gate
        if required_list[required_ind] == gate:
            print("Ate " + gate)
            #screen.pixel(apple_x, apple_y, 0)
            required_ind +=1
            if required_ind == len(required_list):
                success = True
                break
            else:
                gate,width,height=return_gates()

        else:
            break
        while (apple_x, apple_y) in snake:
            apple_x = random.randint(2,high=int(screen_size/2))
            apple_y = random.getrandbits(2,high=int(screen_size/2))
        #screen.pixel(apple_x, apple_y, 2)
        #game_speed += 0.2
    x, y = snake.pop(0)
    screen.pixel(x, y, 0)
    #x, y = snake.pop(0)
    #screen.pixel(x, y, 0)


if success is False:
    text = pew.Pix.from_text("Game over!")
else:
    text = pew.Pix.from_text("You win!")
for dx in range(-screen_size[0], text.width):
    screen.blit(text, -dx, int(screen_size[1]/2))
    pew.show(screen)
    pew.tick(1 / 12)
