from PPlay.gameimage import GameImage
from time import time
from math import atan2, cos, sin, sqrt
from PPlay.animation import Animation
from PPlay.window import *
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 45
        self.height = 48

        # Carrega animações para movimento
        self.image_right = Animation("../images/characters/player_right.png", 3)
        self.image_right.set_sequence(0, 2, loop=True)
        self.image_right.set_total_duration(500)

        self.image_left = Animation("../images/characters/player_left.png", 3)
        self.image_left.set_sequence(0, 2, loop=True)
        self.image_left.set_total_duration(500)

        self.image_down = Animation("../images/characters/player_down.png", 3)
        self.image_down.set_sequence(0, 2, loop=True)
        self.image_down.set_total_duration(500)

        self.image_up = Animation("../images/characters/player_up.png", 3)
        self.image_up.set_sequence(0, 2, loop=True)
        self.image_up.set_total_duration(500)

        # Animações de ataque
        self.attack_right = Animation("../images/characters/player_attack_right.png", 5)
        self.attack_right.set_sequence(0, 4, loop=False)
        self.attack_right.set_total_duration(700)

        self.attack_left = Animation("../images/characters/player_attack_left.png", 5)
        self.attack_left.set_sequence(0, 4, loop=False)
        self.attack_left.set_total_duration(700)

        self.attack_down = Animation("../images/characters/player_attack_down.png", 5)
        self.attack_down.set_sequence(0, 4, loop=False)
        self.attack_down.set_total_duration(700)

        self.attack_up = Animation("../images/characters/player_attack_up.png", 5)
        self.attack_up.set_sequence(0, 4, loop=False)
        self.attack_up.set_total_duration(700)

        # Animações paradas (idle)
        self.idle_right = Animation("../images/characters/player_idle_right.png", 2)
        self.idle_right.set_sequence(0, 1, loop=True)
        self.idle_right.set_total_duration(1000)

        self.idle_left = Animation("../images/characters/player_idle_left.png", 2)
        self.idle_left.set_sequence(0, 1, loop=True)
        self.idle_left.set_total_duration(1000)

        self.idle_down = Animation("../images/characters/player_idle_down.png", 2)
        self.idle_down.set_sequence(0, 1, loop=True)
        self.idle_down.set_total_duration(500)

        self.idle_up = Animation("../images/characters/player_idle_up.png", 2)
        self.idle_up.set_sequence(0, 1, loop=True)
        self.idle_up.set_total_duration(1000)

        # Define imagem inicial como movimento para baixo (idle)
        self.current_image = self.idle_down

        # Configuração de velocidade e dash
        self.speed = 200
        self.dash_speed = 400
        self.dash_duration = 0.2
        self.dash_cooldown = 0.8
        self.is_dashing = False
        self.last_dash_time = 0

        # Configuração de vidas e invencibilidade
        self.lives = 5
        self.invincible_time = 0
        self.invincible_duration = 2
        self.is_invincible = False
        self.is_visible = True
        self.blink_interval = 0.08
        self.last_blink_time = 0

        # Chave do jogador
        self.has_key = False

        # Controle de ataque
        self.attack_cooldown = 1.0  # Intervalo de 2 segundos entre ataques
        self.last_attack_time = 0  # Tempo do último ataque
        self.is_attacking = False
        self.attack_start_time = 0

        self.is_moving = False

    def move_left(self, dt):
        from PPlay.mouse import Mouse
        mouse = Mouse()

        if self.is_attacking:  # Se estiver atacando, só atualiza o frame de ataque
            self.last_attack_time -= dt
            if self.last_attack_time <= 0:
                self.is_attacking = False
            else:
                self.current_image = self.attack_left
                self.attack_left.update()
                return

        # Se não estiver atacando, verifica o movimento normal
        self.x -= self.dash_speed * dt if self.is_dashing else self.speed * dt
        self.is_moving = True
        if mouse.is_button_pressed(1):
            self.is_attacking = True
            self.last_attack_time = self.attack_cooldown
            self.current_image = self.attack_left
        else:
            self.current_image = self.image_left
        self.current_image.update()

    def move_right(self, dt):
        from PPlay.mouse import Mouse
        mouse = Mouse()

        if self.is_attacking:  # Se estiver atacando, só atualiza o frame de ataque
            self.last_attack_time -= dt
            if self.last_attack_time <= 0:
                self.is_attacking = False
            else:
                self.current_image = self.attack_right
                self.attack_right.update()
                return

        # Se não estiver atacando, verifica o movimento normal
        self.x += self.dash_speed * dt if self.is_dashing else self.speed * dt
        self.is_moving = True
        if mouse.is_button_pressed(1):
            self.is_attacking = True
            self.last_attack_time = self.attack_cooldown
            self.current_image = self.attack_right
        else:
            self.current_image = self.image_right
        self.current_image.update()

    def move_up(self, dt):
        from PPlay.mouse import Mouse
        mouse = Mouse()

        if self.is_attacking:  # Se estiver atacando, só atualiza o frame de ataque
            self.last_attack_time -= dt
            if self.last_attack_time <= 0:
                self.is_attacking = False
            else:
                self.current_image = self.attack_up
                self.attack_up.update()
                return

        # Se não estiver atacando, verifica o movimento normal
        self.y -= self.dash_speed * dt if self.is_dashing else self.speed * dt
        self.is_moving = True
        if mouse.is_button_pressed(1):
            self.is_attacking = True
            self.last_attack_time = self.attack_cooldown
            self.current_image = self.attack_up
        else:
            self.current_image = self.image_up
        self.current_image.update()

    def move_down(self, dt):
        from PPlay.mouse import Mouse
        mouse = Mouse()

        if self.is_attacking:  # Se estiver atacando, só atualiza o frame de ataque
            self.last_attack_time -= dt
            if self.last_attack_time <= 0:
                self.is_attacking = False
            else:
                self.current_image = self.attack_down
                self.attack_down.update()
                return

        # Se não estiver atacando, verifica o movimento normal
        self.y += self.dash_speed * dt if self.is_dashing else self.speed * dt
        self.is_moving = True
        if mouse.is_button_pressed(1):
            self.is_attacking = True
            self.last_attack_time = self.attack_cooldown
            self.current_image = self.attack_down
        else:
            self.current_image = self.image_down
        self.current_image.update()

    def dash(self):
        # Executa o dash se estiver fora do cooldown
        current_time = time()
        if current_time - self.last_dash_time > self.dash_cooldown and not self.is_dashing:
            self.is_dashing = True
            self.last_dash_time = current_time

    def lose_life(self):
        """
        Perde uma vida e ativa invencibilidade.
        """
        if self.lives > 0 and not self.is_invincible:
            self.lives -= 1
            self.is_invincible = True
            self.invincible_time = time()
            self.is_visible = True  # Garante que o jogador comece visível

        if self.lives == 0:  # Verifica se as vidas acabaram
            self.game_over()

    def game_over(self):
        from menu import Main_menu
        game_status = False
        window = Window(1200, 900)
        keyboard = window.get_keyboard()
        lose = GameImage("../images/menu/game over.jpg")
        lose.x = 0
        lose.y = 0
        while True:
            lose.draw()
            window.update()
            if keyboard.key_pressed("ESC"):
                window.close()


    def update(self, dt):
        """
        Atualiza o estado do jogador a cada quadro.
        """
        current_time = time()

        # Verifica o estado de invencibilidade
        if self.is_invincible:
            # Verifica se o tempo de invencibilidade terminou
            if current_time - self.invincible_time > self.invincible_duration:
                self.is_invincible = False
                self.is_visible = True  # Garante que o jogador volte a ficar visível
            else:
                # Alterna a visibilidade em intervalos de "blink_interval"
                if current_time - self.last_blink_time >= self.blink_interval:
                    self.is_visible = not self.is_visible  # Alterna entre visível/invisível
                    self.last_blink_time = current_time

        # Verifica a animação de ataque
        if self.is_attacking:
            if not self.current_image.is_playing():  # Se a animação terminou
                self.is_attacking = False
                if self.current_image in [self.attack_right, self.image_right]:
                    self.current_image = self.idle_right
                elif self.current_image in [self.attack_left, self.image_left]:
                    self.current_image = self.idle_left
                elif self.current_image in [self.attack_up, self.image_up]:
                    self.current_image = self.idle_up
                elif self.current_image in [self.attack_down, self.image_down]:
                    self.current_image = self.idle_down

        # Verifica o estado do dash
        if self.is_dashing:
            if time() - self.last_dash_time > self.dash_duration:
                self.is_dashing = False

        # Verifica se o jogador não está se movendo e atualiza para animação idle
        if not self.is_attacking:
            if not self.is_moving:  # Se não está se movendo
                if self.current_image in [self.image_right, self.attack_right]:
                    self.current_image = self.idle_right
                elif self.current_image in [self.image_left, self.attack_left]:
                    self.current_image = self.idle_left
                elif self.current_image in [self.image_up, self.attack_up]:
                    self.current_image = self.idle_up
                elif self.current_image in [self.image_down, self.attack_down]:
                    self.current_image = self.idle_down

        # Atualiza a animação atual
        self.current_image.update()

        # Reinicia o estado de movimento
        self.is_moving = False

    def draw(self):
        """
        Desenha o jogador apenas se ele estiver visível.
        """
        if self.is_visible:
            self.current_image.x = self.x
            self.current_image.y = self.y
            self.current_image.draw()

    def get_sprite(self):
        # Retorna a imagem atual do jogador
        return self.current_image

    def attack(self, enemies):
        """
        Realiza o ataque e aplica dano baseado na proximidade dos inimigos.
        :param enemies: Lista de inimigos no jogo.
        """
        current_time = time()

        # Verifica se o ataque está disponível (cooldown)
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            self.is_attacking = True
            self.attack_start_time = current_time


            # Define animação de ataque baseada na última direção
            if self.current_image in [self.image_right, self.idle_right]:
                self.current_image = self.attack_right
            elif self.current_image in [self.image_left, self.idle_left]:
                self.current_image = self.attack_left
            elif self.current_image in [self.image_up, self.idle_up]:
                self.current_image = self.attack_up
            elif self.current_image in [self.image_down, self.idle_down]:
                self.current_image = self.attack_down

            # Reinicia a animação de ataque
            self.current_image.set_sequence(0, 4, loop=False)  # Garante que a sequência seja configurada corretamente
            self.current_image.stop()  # Para qualquer animação anterior
            self.current_image.play()  # Reinicia a animação do ataque

            # Verifica inimigos atingidos
            for enemy in enemies:
                distance = sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)

                # Aplica dano baseado na proximidade
                min_distance = 0.5
                max_distance = 100
                if min_distance < distance < max_distance:
                    damage = max(0, (151 - distance))  # Garante que o dano não seja negativo
                    enemy.take_damage(damage, self)  # Aplica dano no inimigo
