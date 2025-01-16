def fadeout():
    fadeout = pg.Surface((screen_width, screen_height))
    fadeout = fadeout.convert()
    fadeout.fill(black)
    for i in range(255):
        fadeout.set_alpha(i)
        screen.blit(fadeout, (0, 0))
        pg.display.update()


def fadein():
    fadein = pg.Surface((screen_width, screen_height))
    fadein = fadein.convert()
    fadein.fill(black)
    for i in range(255):
        fadein.set_alpha(255-i)
        screen.blit(fadein, (0, 0))
        pg.display.update()