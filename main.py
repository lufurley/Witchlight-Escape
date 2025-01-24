from menu import Main_menu
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.keyboard import *
from player import Player
from rooms import RoomLibrary
from PPlay.mouse import *
from PPlay.collision import Collision
from math import *
from PIL import Image
from objects import Key
from PPlay.sound import *

# Call the menu first
menu_choice = Main_menu()

if menu_choice == "play":
    # Configuração inicial da janela do jogo
    window = Window(1200, 900)  # Define o tamanho da janela
    window.set_title("Witchlight Escape")  # Título da janela
    keyboard = Keyboard()  # Objeto para controle via teclado
    mouse = Mouse()  # Objeto para controle via mouse

    scroll_image = GameImage("../images/objects/pergaminho.png")
    scroll_image.x = window.width / 2 - scroll_image.width / 2
    scroll_image.y = window.height / 2 - scroll_image.height / 2

    ok_button = GameImage("../images/objects/botao_ok.png")
    ok_button.x = scroll_image.x + scroll_image.width / 2 - ok_button.width / 2
    ok_button.y = scroll_image.y + scroll_image.height - ok_button.height - 50
    # Lógica para exibir o pergaminho

    display_scroll = True

    while display_scroll:
        scroll_image.draw()  # Desenha o pergaminho
        ok_button.draw()  # Desenha o botão OK

        # Verifica se o botão OK foi clicado
        if mouse.is_button_pressed(1):
            if (
                    mouse.is_over_object(ok_button)
            ):  # Verifica se o mouse está sobre o botão OK
                display_scroll = False  # Sai do loop de exibição do pergaminho

        window.update()  # Atualiza a tela

    '''Som de fundo da gameplay'''
    dungeon_song = Sound("../efeitos_sonoros/dungeon-song.mp3")
    dungeon_song.set_volume(50)
    dungeon_song.loop = True
    dungeon_song.stop()
    dungeon_song.play()

    play_song = Sound("../efeitos_sonoros/play.mp3")
    play_song.set_volume(30)
    play_song.loop = True
    play_song.stop()
    play_song.play()

    new_room = Sound("../efeitos_sonoros/new_room.mp3")
    damage_song = Sound("../efeitos_sonoros/damage_player.mp3")
    laugh_wizard = Sound("../efeitos_sonoros/wizard_laugh.mp3")
    attack_player = Sound("../efeitos_sonoros/attack_song.mp3")

    # Criação do objeto chavewd
    key = Key(400, 300)

    # Inicialização do jogador
    player = Player(250, 425)  # Define a posição inicial do jogador

    # Carrega o quarto inicial
    room_library = RoomLibrary()
    current_room_id = 1  # ID da sala inicial
    current_room = room_library.get_room(current_room_id)  # Dados da sala inicial
    background = current_room['background']  # Fundo da sala
    mask_image = current_room['mask']  # Máscara de colisão da sala
    mask_pixels = mask_image.load()  # Dados de pixels da máscara

    # Carrega a imagem de vidas
    life_image = GameImage("../images/objects/heart.png")
    life_size = 40

    def check_room_transition_to_12():
        global current_room, current_room_id, background, mask_image, mask_pixels, vampires, skeletons, skulls, boss, key

        # Verifica se o jogador possui a chave e está tentando entrar na sala 12

        if player.has_key == False:
            if player.y + player.height + 10 > window.height:
                player.y = window.height - player.height - 10

        elif player.has_key and current_room_id == 10:
            if player.y + player.height > window.width:  # Tentando sair pela direita
                next_room_id = current_room.get('down')

                if next_room_id == 12:  # Transição para a sala 12
                    '''Sons de Entrada na sala 12'''
                    play_song.stop()
                    laugh_wizard.play()
                    laugh_wizard.stop()

                    current_room = room_library.get_room(next_room_id)
                    current_room_id = next_room_id
                    background = current_room['background']
                    mask_image = current_room['mask']
                    mask_pixels = mask_image.load()

                    reset_player_position()

                    # Configura inimigos da sala 12
                    vampires, skeletons, skulls, boss = room_library.spawn_enemies(next_room_id)
    def draw_lives():
        """Desenha as vidas restantes do jogador no canto superior esquerdo da tela."""
        for i in range(player.lives):
            life_image.x = 10 + i * (life_size + 10)  # Define a posição horizontal
            life_image.y = 10  # Define a posição vertical
            life_image.draw()  # Renderiza a imagem

    def is_valid_position(x, y, width, height):
        """Verifica se uma posição está dentro do caminho válido na máscara."""
        for dx in range(int(width)):
            for dy in range(int(height)):
                nx = x + dx
                ny = y + dy

                if 0 <= nx < mask_image.width and 0 <= ny < mask_image.height:
                    if mask_pixels[int(nx), int(ny)] <= 200:  # Define o limite de colisão
                        return False
        return True

    def check_collisions(player, enemies):
        """ Verifica colisões entre o jogador e inimigos ativos."""
        for enemy in enemies:
            if not player.is_invincible and not enemy.is_dead:
                player_box = {
                    "x": player.x,
                    "y": player.y,
                    "width": player.width,
                    "height": player.height
                }
                enemy_box = {
                    "x": enemy.x,
                    "y": enemy.y,
                    "width": enemy.width,
                    "height": enemy.height
                }

                if (
                    player_box["x"] < enemy_box["x"] + enemy_box["width"]
                    and player_box["x"] + player_box["width"] > enemy_box["x"]
                    and player_box["y"] < enemy_box["y"] + enemy_box["height"]
                    and player_box["y"] + player_box["height"] > enemy_box["y"]
                ):
                    '''Som de dano ao player'''
                    damage_song.set_volume(20)
                    damage_song.stop()
                    damage_song.play()
                    player.lose_life()

    # Lista de inimigos ativos na sala atual
    vampires = []
    skeletons = []
    skulls = []
    # Inicializa a variável do chefe
    wizard = []
    room_library.mark_room_complete(current_room_id)  # Marca a sala inicial como completa


    def reset_player_position():
        '''Som de avanço para a nova sala'''
        new_room.set_volume(20)
        new_room.stop()
        new_room.play()
        """Reposiciona o jogador para o lado oposto ao qual saiu."""
        if player.x + player.width < 0:  # Saiu pela esquerda
            player.x = window.width - player.width
        elif player.x > window.width:  # Saiu pela direita
            player.x = 0
        elif player.y < 0:  # Saiu pelo topo
            player.y = window.height - player.height - 5
        elif player.y + player.height + 3 > window.height:  # Saiu pelo fundo
            player.y = 0  # Reaparece no topo da nova sala


    def check_room_transition():
        global current_room, current_room_id, background, mask_image, mask_pixels, vampires, skeletons, skulls, wizard

        # Combina todos os inimigos da sala atual
        all_enemies = vampires + skeletons + skulls + wizard

        # Verifica se todos os inimigos estão mortos antes de permitir a transição
        if all(enemy.is_dead for enemy in all_enemies):
            room_library.mark_room_complete(current_room_id)
            next_room_id = None

            # Detecta saída pelas bordas
            if player.x + player.width < 0:  # Saiu pela esquerda
                next_room_id = current_room.get('left')
            elif player.x > window.width:  # Saiu pela direita
                next_room_id = current_room.get('right')
            elif player.y < 0:  # Saiu pelo topo
                next_room_id = current_room.get('up')
            elif player.y + player.height + 3 > window.height:  # Saiu pelo fundo
                next_room_id = current_room.get('down')

            if next_room_id:
                # Carrega a nova sala
                current_room = room_library.get_room(next_room_id)
                current_room_id = next_room_id
                background = current_room['background']
                mask_image = current_room['mask']
                mask_pixels = mask_image.load()

                # Reposiciona o jogador
                reset_player_position()

                # Configura os inimigos da nova sala
                vampires, skeletons, skulls, wizards = room_library.spawn_enemies(next_room_id)
                wizard = wizards
        else:
            # Impede saída se houver inimigos vivos
            if player.x < 0:
                player.x = 0
            elif player.x + player.width > window.width:
                player.x = window.width - player.width
            elif player.y < 0:
                player.y = 0
            elif player.y + player.height > window.height:
                player.y = window.height - player.height


    # Loop principal do jogo
    while True:
        dt = window.delta_time()  # Calcula o tempo desde o último frame

        # Movimentação do jogador com validação de posição
        if keyboard.key_pressed("a"):
            if is_valid_position(player.x - player.speed * dt, player.y, player.width, player.height):
                player.move_left(dt)
        if keyboard.key_pressed("d"):
            if is_valid_position(player.x + player.speed * dt, player.y, player.width, player.height):
                player.move_right(dt)
        if keyboard.key_pressed("w"):
            if is_valid_position(player.x, player.y - player.speed * dt, player.width, player.height):
                player.move_up(dt)
        if keyboard.key_pressed("s"):
            if is_valid_position(player.x, player.y + player.speed * dt, player.width, player.height):
                player.move_down(dt)

        # Combina todos os inimigos ativos, incluindo o boss (wizard)
        all_enemies = vampires + skeletons + skulls + wizard  # Adiciona o boss à lista de inimigos

        # Ataca ao clicar com o botão esquerdo do mouse
        if mouse.is_button_pressed(1):
            attack_player.set_volume(30)
            attack_player.stop()
            attack_player.play()
            player.attack(all_enemies)

        # Executa o dash ao clicar com o botão direito do mouse
        if mouse.is_button_pressed(3):
            player.dash()

        player.update(dt)  # Atualiza o estado do jogador
        check_collisions(player, all_enemies)  # Verifica colisões com todos os inimigos

        if key:
            key.collect(player)  # Verifica se o jogador pegou a chave
            key.draw()  # Desenha a chave

        check_room_transition_to_12()  # Verifica transição para a sala 12
        check_room_transition()  # Verifica transição geral de salas

        background.draw()  # Renderiza o fundo da sala

        # Gerencia a chave da sala atual
        key = current_room.get('key')
        if key:
            key.collect(player)
            key.draw()
            key.update()

        draw_lives()  # Desenha as vidas restantes

        # Atualiza e desenha todos os inimigos vivos, incluindo o boss
        for enemy in all_enemies:
            if not enemy.is_dead:
                enemy.update(dt, player)
                enemy.draw()

        player.draw()  # Desenha o jogador
        window.update()  # Atualiza a tela


