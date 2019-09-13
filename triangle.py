import pew

pew.init()
screen = pew.Pix()

def display_mountain():
for i in range(0,8):
    screen.pixel(i,7,3)

for i in range(1,5):
    screen.pixel(8-i+1,8-i,3)
    screen.pixel(i-1,8-i,3)

loc_pixel = 0 
screen.pixel(loc_pixel,0,1)
game_play = True
while game_play is True:

    keys = pew.keys()
    print(keys)
    if keys != 0:
        if keys&pew.K_RIGHT:
            screen.pixel(loc_pixel,0,0)
            loc_pixel = loc_pixel +1
            screen.pixel((loc_pixel)%8,0,1)
        elif keys&pew.K_LEFT:
            screen.pixel(loc_pixel,0,0)
            loc_pixel = loc_pixel -1
            screen.pixel((loc_pixel)%8,0,1)
        if game

    pew.show(screen)
    pew.tick(1/6)

text = pew.Pix.from_text("Game over!")
for dx in range(-8, text.width):
    screen.blit(text, -dx, 1)
    pew.show(screen)
    pew.tick(1 / 12)
