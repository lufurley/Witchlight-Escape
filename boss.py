from PPlay.animation import *
from time import time
import random

from PPlay.animation import Animation
from time import time
import random

from PPlay.animation import *
from time import time
import random

from PPlay.animation import Animation
from time import time
import random

from PPlay.window import *
from PPlay.gameimage import GameImage
from PPlay.sound import *


class Wizard:
    def __init__(self, x, y):
        """Inicializa o chefe final."""
        self.x = x
        self.y = y
        self.width = 53
        self.height = 53
        self.health = 800
        self.is_dead = False
        self.speed = 30
        self.is_damaged = False
        self.damage_timer = 0
        self.projectiles = []

        # Animação do chefe andando para a direita
        self.walk_right_animation = Animation("../images/characters/wizard_right.png", 4)
        self.walk_right_animation.set_sequence(0, 3, loop=True)
        self.walk_right_animation.set_total_duration(1000)

        # Animação do chefe andando para a esquerda
        self.walk_left_animation = Animation("../images/characters/wizard_left.png", 4)
        self.walk_left_animation.set_sequence(0, 3, loop=True)
        self.walk_left_animation.set_total_duration(1000)

        # Animação para o teleporte
        self.teleport_animation_right = Animation("../images/characters/wizard_spell_right.png", 4)
        self.teleport_animation_right.set_sequence(0, 3, loop=False)
        self.teleport_animation_right.set_total_duration(500)  # Animação de teleporte mais rápida

        self.teleport_animation_left = Animation("../images/characters/wizard_spell_left.png", 4)
        self.teleport_animation_left.set_sequence(0, 3, loop=False)
        self.teleport_animation_left.set_total_duration(1000)  # Animação de teleporte mais rápida

        # Inicializa com a animação para a direita
        self.current_animation = self.walk_right_animation
        self.attack_cooldown = 2.0  # Tempo entre ataques (em segundos)
        self.last_attack_time = 0

        # Definir tempo de teleporte
        self.teleport_cooldown = 7.0  # Intervalo entre teletransportes (em segundos)
        self.last_teleport_time = time()

        # Variáveis para controlar direção do movimento
        self.is_moving_right = True
        self.is_moving = False  # Flag para verificar se está se movendo
        self.is_teleporting = False  # Flag para verificar se está no processo de teleporte

        # Variáveis para controle do ataque de magia
        self.magic_attack_cooldown = 2.0  # Tempo entre cada sequência de disparos
        self.last_magic_attack_time = time()
        self.magic_shots_fired = 0  # Contador de disparos de magia
        self.max_magic_shots = 5  # Número máximo de disparos consecutivos
        self.magic_shot_speed = 0.5  # Intervalo entre os disparos consecutivos (rápido)
        self.magic_attack_timer = 0  # Temporizador para o controle de ataques rápidos
        self.is_casting_magic = False  # Verifica se está realizando a animação de magia

        # Cooldown para o ataque especial
        self.special_attack_cooldown = 12.0  # Tempo entre ataques especiais (em segundos)
        self.last_special_attack_time = time()

        self.is_backstepping = False  # Indica se o chefe está recuando
        self.backstep_timer = 0  # Tempo inicial do backstep
        self.backstep_duration = 0.3  # Duração do backstep (em segundos)
        self.backstep_speed = 100  # Velocidade do recuo



    def update(self, dt, player):
        """Atualiza o estado do Wizard"""
        if self.is_damaged:
            if time() - self.damage_timer > 0.2:  # Piscar por 0.2 segundos
                self.is_damaged = False

        # Verifica se está na hora de iniciar o teleporte
        if time() - self.last_teleport_time > self.teleport_cooldown and not self.is_teleporting:
            self.start_teleport_phase = "before"  # Fase inicial do teleporte
            self.is_teleporting = True
            self.last_teleport_time = time()

        # Gerenciar o processo de teleporte
        if self.is_teleporting:
            # Fase antes do teleporte: exibir animação antes do teleporte
            if self.start_teleport_phase == "before":
                if player.x > self.x:
                    self.current_animation = self.teleport_animation_right
                elif player.x < self.x:
                    self.current_animation = self.teleport_animation_left
                self.is_moving = False  # Para o movimento
                if time() - self.last_teleport_time > 0.5:  # Após 0.5 segundos
                    self.teleport()  # Executa o teleporte
                    self.start_teleport_phase = "after"  # Avança para a próxima fase
                    self.last_teleport_time = time()

            # Fase depois do teleporte: exibir animação após o teleporte
            elif self.start_teleport_phase == "after":
                if player.x > self.x:
                    self.current_animation = self.teleport_animation_right
                elif player.x < self.x:
                    self.current_animation = self.teleport_animation_left
                self.is_moving = False  # Continua parado
                if time() - self.last_teleport_time > 0.5:  # Após 0.5 segundos
                    self.start_teleport_phase = None  # Finaliza o teleporte
                    self.is_teleporting = False  # Sai do estado de teleporte
                    self.last_teleport_time = time()  # Reinicia o cooldown

        # Comportamento normal se não estiver teleportando
        if not self.is_teleporting:
            distance_to_player = self.get_distance_to_player(player)

            # Se o Wizard estiver a uma distância pequena do Player (10 pixels), ele fica parado
            if distance_to_player < 10:  # Distância para ele parar
                self.stop()  # Fica parado
            else:
                self.move_towards_player(dt, player)  # Movimento para se aproximar do player

        # Controle de ataque de magia com animação de teleporte
        if self.magic_shots_fired < self.max_magic_shots:
            if player.x > self.x:
                self.current_animation = self.teleport_animation_right
                self.teleport_animation_right.update()
            else:
                self.current_animation = self.teleport_animation_left
                self.teleport_animation_left.update()

            if not self.is_teleporting and not self.is_casting_magic:
                # Começar a animação de teleporte para disparar a magia
                self.is_casting_magic = True
                self.last_magic_attack_time = time()
            elif self.is_casting_magic:
                # Após 0.5 segundos de animação, disparar o projétil
                if time() - self.last_magic_attack_time > 0.4:
                    self.shoot_magic(player)  # Dispara o projétil
                    self.is_casting_magic = False
        # Controle de ataque de magia com animação
        if self.is_casting_magic:
            self.current_animation.update()  # Atualiza a animação de magias

        elif self.magic_shots_fired >= self.max_magic_shots:
            # Depois de disparar os 3 feitiços, aguarda o cooldown
            if time() - self.last_magic_attack_time > self.magic_attack_cooldown:
                self.magic_shots_fired = 0  # Reinicia o contador para os próximos disparos
                self.last_magic_attack_time = time()  # Reinicia o tempo para o próximo ataque

        # Atualiza a animação de movimento ou teleporte
        self.current_animation.update()

        # Ataque especial: dispara magia em 8 direções
        if time() - self.last_special_attack_time > self.special_attack_cooldown:
            self.shoot_special_magic()
            self.last_special_attack_time = time()

        # Lógica para backstep
        if self.is_backstepping:
            if time() - self.backstep_timer < self.backstep_duration:
                # Move o chefe na direção oposta ao jogador
                self.x += self.backstep_dx * self.backstep_speed * dt
                self.y += self.backstep_dy * self.backstep_speed * dt
            else:
                self.is_backstepping = False  # Finaliza o backstep

        # Atualiza projéteis
        for projectile in self.projectiles:
            projectile.update(dt, player)  # Atualiza o projetil e verifica colisão
            projectile.draw()

    def start_teleport(self):
        """Inicia o processo de teleporte."""
        self.is_teleporting = True  # Marca o Wizard como em teleporte
        self.start_teleport_phase = "before"  # Fase inicial antes do teleporte

    def stop_teleport(self):
        """Finaliza o teleporte e retorna à animação de caminhada correta."""
        self.is_teleporting = False  # Marca o fim do teleporte
        self.start_teleport_phase = None  # Remove qualquer estado residual
        # Atualiza a animação com base na direção
        if self.is_moving_right:
            self.current_animation = self.walk_right_animation
        else:
            self.current_animation = self.walk_left_animation

    def teleport(self):
        """Teleporta o Wizard para uma posição aleatória na tela."""
        self.x = random.randint(200, 1000 - self.width)  # Posição aleatória dentro da largura da tela
        self.y = random.randint(200, 700 - self.height)  # Posição aleatória dentro da altura da tela

    def get_distance_to_player(self, player):
        """Calcula a distância entre o Wizard e o jogador."""
        return ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5

    def stop(self):
        """Faz o Wizard ficar parado quando estiver perto do player."""
        self.is_moving = False  # Define que o Wizard parou
        # Atualiza a animação com base na direção
        if self.is_moving_right:
            self.current_animation = self.walk_right_animation
        else:
            self.current_animation = self.walk_left_animation

    def move_towards_player(self, dt, player):
        """Faz o Wizard se mover na direção do player"""
        self.is_moving = True  # Marca que está se movendo

        # Verifica a posição relativa para definir a direção
        if player.x > self.x:
            self.x += self.speed * dt  # Move para a direita
            self.current_animation = self.walk_right_animation  # Atualiza animação para a direita

        elif player.x < self.x:
            self.x -= self.speed * dt  # Move para a esquerda
            self.current_animation = self.walk_left_animation  # Atualiza animação para a esquerda

        # Atualiza a posição vertical (subindo ou descendo)
        if player.y > self.y:
            self.y += self.speed * dt  # Move para baixo
        elif player.y < self.y:
            self.y -= self.speed * dt  # Move para cima

        self.walk_right_animation.update()
        self.walk_left_animation.update()

    def shoot_magic(self, player):
        """Realiza o disparo de magia."""
        self.magic_shots_fired += 1  # Incrementa o contador de disparos
        self.magic_attack_timer = time()  # Reseta o tempo do último disparo

        # Ajusta a animação para o disparo
        if player.x > self.x:
            self.current_animation = self.teleport_animation_right
        else:
            self.current_animation = self.teleport_animation_left

        self.current_animation.update()  # Atualiza a animação no momento do disparo

        # Criar e adicionar o projetil
        projectile = MagicProjectile(self.x, self.y, player.x, player.y)
        self.projectiles.append(projectile)

    def shoot_special_magic(self):
        """Dispara magia em 8 direções diferentes."""
        directions = [
            (0, -1),  # Norte
            (0, 1),  # Sul
            (-1, 0),  # Oeste
            (1, 0),  # Leste
            (-1, -1),  # Noroeste
            (1, -1),  # Nordeste
            (-1, 1),  # Sudoeste
            (1, 1)  # Sudeste
        ]

        for dx, dy in directions:
            projectile = MagicProjectile(self.x, self.y, self.x + dx * 100, self.y + dy * 100)
            self.projectiles.append(projectile)

    def take_damage(self, damage, player):
        """Aplica dano ao Wizard e faz ele dar um backstep."""
        if not self.is_dead:
            self.health -= damage
            self.is_damaged = True
            self.damage_timer = time()

            if self.health <= 0:
                self.die()
            else:
                damage_wizard = Sound("../efeitos_sonoros/damage_wizard.mp3")
                damage_wizard.stop()
                damage_wizard.set_volume(30)
                damage_wizard.play()

                # Inicia o backstep
                self.is_backstepping = True
                self.backstep_timer = time()
                # Calcula a direção oposta ao jogador
                self.backstep_dx = self.x - player.x
                self.backstep_dy = self.y - player.y
                distance = (self.backstep_dx ** 2 + self.backstep_dy ** 2) ** 0.5
                self.backstep_dx /= distance
                self.backstep_dy /= distance

    def die(self):

        """Finaliza o boss."""
        self.is_dead = True  # Marca o chefe como morto
        self.current_animation = None  # Opcional: Remover a animação ativa
        self.projectiles.clear()  # Remove todos os projéteis do chefe

        death_wizard = Sound("../efeitos_sonoros/death_wizard.mp3")
        death_wizard.stop()
        death_wizard.set_volume(30)
        death_wizard.play()


        from menu import Main_menu
        game_status = False
        window = Window(1200, 900)
        keyboard = window.get_keyboard()
        win = GameImage("../images/menu/voce venceu.jpg")
        win.x = 0
        win.y = 0
        while True:
            win.draw()
            window.update()
            if keyboard.key_pressed("ESC"):
                window.close()

    def draw(self):
        """Desenha o chefe na tela."""
        if not self.is_dead:
            self.current_animation.x = self.x
            self.current_animation.y = self.y
            self.current_animation.draw()


from PPlay.sprite import Sprite
from PPlay.animation import Animation


class MagicProjectile:
    def __init__(self, x, y, target_x, target_y, is_right=True):
        """Inicializa o projetil de magia."""
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 250  # Velocidade do projetil
        self.target_x = target_x
        self.target_y = target_y
        self.is_dead = False
        self.is_right = is_right  # Direção do projetil

        # Usando Sprite para carregar a imagem do projetil
        self.animation = Animation("../images/objects/spell.png", 3)  # Substitua com a imagem da magia
        self.animation.set_sequence(0, 2, loop=True)
        self.animation.set_total_duration(1000)  # Defina o tempo adequado

        # Calculando a direção do projetil
        self.dx = target_x - self.x
        self.dy = target_y - self.y
        distance = (self.dx ** 2 + self.dy ** 2) ** 0.5
        self.dx /= distance  # Normaliza o vetor
        self.dy /= distance  # Normaliza o vetor

        if not self.is_right:  # Se não for a direção certa (para a esquerda), inverte a direção
            self.dx = -self.dx
            self.dy = -self.dy

    def check_collision(self, player):
        """Verifica se o projetil colidiu com o jogador."""
        # Calcula a distância entre o projetil e o jogador
        dist_x = self.x - player.x
        dist_y = self.y - player.y
        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5

        # Verifica se a distância entre o projetil e o jogador é menor que a soma dos seus raios
        if distance < (self.width / 2 + player.width / 2):
            player.lose_life()  # Faz o jogador perder uma vida
            self.is_dead = True  # Destrói o projetil após a colisão

    def update(self, dt, player):
        """Atualiza o movimento do projetil de magia e verifica colisões."""
        if not self.is_dead:
            self.x += self.dx * self.speed * dt
            self.y += self.dy * self.speed * dt

            # Verifica se o projetil saiu da tela
            if self.x < 0 or self.x > 1024 or self.y < 0 or self.y > 768:
                self.is_dead = True

            # Verifica colisão com o jogador
            self.check_collision(player)

            # Atualiza a animação
            self.animation.x = self.x
            self.animation.y = self.y
            self.animation.update()

    def draw(self):
        """Desenha o projetil de magia na tela."""
        if not self.is_dead:
            self.animation.draw()

