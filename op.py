from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sound import *

def opcoes():
    window = Window(1200, 900)
    window.set_title("../images/menu/Witchlight Escape")
    background = GameImage("../images/menu/menu.jpg")
    click_esc = Sound("../efeitos_sonoros/button.mp3")
    teclado = Window.get_keyboard()

    title = GameImage("../images/menu/title op.png")
    title.x = window.width / 2 - title.width / 2
    title.y = window.height / 5

    controles = GameImage("../images/menu/controles.png")
    controles.x = window.width/6
    controles.y = window.height/3 + controles.height/2 + 45

    mouse = GameImage("../images/menu/mouse.png")
    mouse.x = window.width / 2 + mouse.width/9
    mouse.y = window.height / 3 + mouse.height / 2
    while True:

        if teclado.key_pressed("ESC"):
            click_esc.play()
            return True

        background.draw()
        title.draw()
        controles.draw()
        mouse.draw()
        window.update()