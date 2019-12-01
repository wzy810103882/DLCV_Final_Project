import pygame, sys
from PIL import Image
pygame.init()

def displayImage(screen, px, topleft, prior):
    # ensure that the rect always has positive width, height
    x, y = topleft
    width =  pygame.mouse.get_pos()[0] - topleft[0]
    height = pygame.mouse.get_pos()[1] - topleft[1]
    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
    current = x, y, width, height
    if not (width and height):
        return current
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)


def setup(path):
    px = pygame.image.load(path)
    screen = pygame.display.set_mode( px.get_rect()[2:] )
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px

def mainLoop(screen, px):
    topleft = bottomright = prior = None
    n=0
    while n!=1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if not topleft:
                    topleft = event.pos
                else:
                    bottomright = event.pos
                    n=1
            if event.type == pygame.QUIT:
                n = 1
                #pygame.display.quit()
                #pygame.quit()
                #quit()   

        if topleft:
            prior = displayImage(screen, px, topleft, prior)
    return ( topleft + bottomright )

if __name__ == "__main__":
    background_loc = 'Data/background/background_001_small.png'
    human_loc = 'Data/insert/human_001.png'

    screen, px = setup(background_loc)
    left, upper, right, lower = mainLoop(screen, px)

    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower 

    background = Image.open(background_loc)
    human = Image.open(human_loc)
    real = background.copy() 
    #print(upper)
    #print(lower)
    human_background_ratio = abs(upper - lower)  / background.size[1]
    scale = background.size[0] * human_background_ratio / human.size[0]

    width, height = int(human.size[0] * scale), int(human.size[1] * scale)
    #print(width)
    #print(height)
    human = human.resize((width, height), Image.ANTIALIAS)
    #human.show()

    bg_width, bg_height = background.size
    x = left
    y = upper
    #x_ratio = 0.7
    #y_ratio = 0.7
    #x = int(x_ratio * bg_width)
    #y = int(y_ratio * bg_height)

    background.paste(human, (x, y), human)
    #background.save("SinGAN/Input/Harmonization/human.png")

    #background.show()

    ref = background.copy() 

    background = Image.new('RGB', (bg_width, bg_height))

    human_width, human_height = human.size
    human_mask = Image.new('RGBA', (human_width,human_height), (0, 0, 0, 0))

    for i in range(human_width):
        for j in range(human_height):
            _,_,_,a = human.getpixel((i,j))
            if a != 0:
                human_mask.putpixel((i,j), (255,255,255,255))

    #human_mask.show()

    background.paste(human_mask, (x, y), human_mask)
    mask = background.copy()
    #background.show()
    #background.save("SinGAN/Input/Harmonization/human_mask.png")


    # ensure output rect always has positive width, height
    

    #im = im.crop(( left, upper, right, lower))

    pygame.display.quit()


    ref_loc = 'Data/harmonization/ref.png'
    real_loc = 'Data/harmonization/real.png' # background 
    mask_loc = 'Data/harmonization/mask.png'

    ref.save(ref_loc)
    real.save(real_loc)
    mask.save(mask_loc)


