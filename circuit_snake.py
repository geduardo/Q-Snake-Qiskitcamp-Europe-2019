import pew
import random


pew.init()
screen = pew.Pix()

game_speed = 4
snake = [(2, 4)]
dx, dy = 1, 0

res = 680,680
screen_size = int(res[0]/40),int(res[1]/40) 

def plot_box(x,y,width,height):
    for i in range(x, x+width):
        for j in [y, y+height]:
            screen.pixel(i,j,1)
    for i in [x, x+width]:
        for j in range(y, y+height):
            screen.pixel(i,j,1)


def print_gate(gate,apple_x,apple_y):
    text = pew.Pix.from_text(gate[:2])
    screen.blit(text,apple_x,apple_y)
    width= text.width
    height = text.height
    plot_box(x=apple_x-1,y=apple_y-1,width=width,height=height)
    return width, height

def return_gates():
    list_gates = ["Hadamard","Rotate","Measurement"]
    gate_ind = random.randint(0,len(list_gates)-1)
    gate = list_gates[gate_ind] 
    width,height = print_gate(gate,apple_x,apple_y)
    return gate,width,height

apple_x, apple_y = int(screen_size[0]/2), int(screen_size[1]/2)
gate,width,height= return_gates()
screen.pixel(apple_x, apple_y, 2)


required_list = ["Hadamard","Rotate","Measurement"]
required_ind = 0

success = False

while True:
    if len(snake) > 1:
        x, y = snake[-2]
        screen.pixel(x, y, 1)
    x, y = snake[-1]
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

    if keys & pew.K_O:
        gate,width,height= return_gates()
        #screen.pixel(apple_x, apple_y, 1)

    #if (x, y) in snake:
    #    break
    snake.append((x, y))

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
    else:
        x, y = snake.pop(0)
        screen.pixel(x, y, 0)


if success is False:
    text = pew.Pix.from_text("Game over!")
else:
    text = pew.Pix.from_text("You win!")
for dx in range(-screen_size[0], text.width):
    screen.blit(text, -dx, int(screen_size[1]/2))
    pew.show(screen)
    pew.tick(1 / 12)
