
import pew
import random
pew.init()
screen = pew.Pix()
#Selecting game speed
game_speed = 5
#Selecting initial position of the snake
snake = [(3,3)]
#Selecting initial velocity of the snake
dx, dy = 1, 0
#Selecting initial position of the apple
apple_x, apple_y = 6, 4
screen.pixel(apple_x, apple_y, 3)
##Now let's implement a loop for the game
while True:
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

    # #Let's create a barrier
    # size_barrier=3
    # y_position_barrier=6
    # x_position_barrier=2
    # barrier=[(x_position_barrier,y_position_barrier)]
    
    for i in range(0,size_barrier):
        barrier.append(((x+i),y))
        screen.pixel(x_position_barrier+i,y_position_barrier,2)

    #Now we define a loop to end the loop (and the game) if the next position
    # of the head is in the snake or it goes out of the grid
    if (x, y) in snake or x==9 or y==9 or x==-1 or y==-1:
        #Here we turn of all the pixles from the snake and the apple
        for (i,j) in snake:
            screen.pixel(i,j,0)
        screen.pixel(apple_x,apple_y,0)
        break
    #If none of those thing happens the head of the snake gets updated to the new position
    snake.append((x, y))

    #Now we create a conditional loop for changing the size and spawning new apples depending
    # on if the snake eats the apple or not
    if x == apple_x and y == apple_y:
        #If the snake eats the apple we turn of the pixel of the apple
        screen.pixel(apple_x, apple_y, 0)
        #Now we define the coordinates of the apple to lie inside the snake for the loop
        apple_x, apple_y = snake[0]
        #We create a loop to generate an apple ouside the snake
        while (apple_x, apple_y) in snake:

            apple_x = random.getrandbits(3)

            apple_y = random.getrandbits(3)
        #We light the pixels of the new apple
        screen.pixel(apple_x, apple_y, 2)
        #We increase the speed of the game 
        game_speed += 0.2
    #If the snake eats the apple we don't delete the last pixel of the snake. Otherwise we remove
    # the last pixel to not increase the size of the snake
    else:

        x, y = snake.pop(0)

        screen.pixel(x, y, 0)

#When the loop is finished we print the game over screen
text = pew.Pix.from_text("Game over!")

for dx in range(-8, text.width):

    screen.blit(text, -dx, 1)

    pew.show(screen)

    pew.tick(1 / 12)