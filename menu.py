from PPlay.window import *
from PPlay.gameimage import *
from PPlay.mouse import Mouse
from op import opcoes
from PPlay.sound import *

def Main_menu():
    game_status = True
    window = Window(1200, 900)
    window.set_title("Witchlight Escape")
    background = GameImage("../images/menu/menu.jpg")
    mouse = window.get_mouse()

    click_mouse = Sound("../efeitos_sonoros/button.mp3")
    menu_song = Sound("../efeitos_sonoros/menu_song.mp3")
    menu_song.loop = True
    menu_song.play()

    title = GameImage("../images/menu/WITCHLIGHT.png")
    title2 = GameImage("../images/menu/ESCAPE.png")
    title.x = window.width / 2 - title.width / 2 + 15
    title.y = window.height / 8
    title2.x = (window.width / 2 - title2.width / 2)
    title2.y = window.height / 12 + title2.height / 2 + title.y + 40

    play = GameImage("../images/menu/playbutton.png")
    play.x = window.width / 2 - play.width / 2
    play.y = window.height / 3 + play.height + 100

    option = GameImage("../images/menu/optionsbutton.png")
    option.x = window.width / 2 - option.width / 2
    option.y = play.y + play.height

    sair = GameImage("../images/menu/sairbutton.png")
    sair.x = window.width / 2 - sair.width / 2
    sair.y = option.y + option.height

    menu = True

    while menu:
        # Options menu (play, options, exit)
        if mouse.is_over_object(play) and mouse.is_button_pressed(1):
            click_mouse.play()
            menu_song.stop()
            return "play"  # Start the game
        if mouse.is_over_object(option) and mouse.is_button_pressed(1):
            click_mouse.play()
            opcoes()  # Open the options
        if mouse.is_over_object(sair) and mouse.is_button_pressed(1):
            click_mouse.play()
            window.close()  # Exit the game
            menu = False

        background.draw()
        play.draw()
        option.draw()
        sair.draw()
        title2.draw()
        title.draw()
        window.update()
