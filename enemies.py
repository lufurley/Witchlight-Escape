from PPlay.gameimage import GameImage
from time import time
from math import atan2, cos, sin, sqrt, pi, degrees
from PPlay.animation import Animation
from PPlay.sound import *


class Skeleton:
    def __init__(self, x, y, patrol_range=100):
        """Inicializa o esqueleto com posição, animações e comportamento de patrulha."""
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        # Configura as animações de caminhada
        self.walking_animation_right = Animation("../images/characters/skeleton_right.png", 4)
        self.walking_animation_right.set_sequence(0, 3, loop=True)
        self.walking_animation_right.set_total_duration(1000)
        self.walking_animation_left = Animation("../images/characters/skeleton_left.png", 4)
        self.walking_animation_left.set_sequence(0, 3, loop=True)
        self.walking_animation_left.set_total_duration(1000)
        self.current_image = self.walking_animation_right
        self.speed = 50
        self.health = 300
        self.is_dead = False
        self.patrol_range = patrol_range
        self.start_x = x
        self.direction = 1

        # Variáveis de controle de backstep
        self.is_backstepping = False
        self.backstep_duration = 0.2  # Duração do backstep (em segundos)
        self.backstep_distance = 20  # Distância do backstep (em pixels)
        self.backstep_timer = 0

    def patrol(self, dt):
        """Movimenta o esqueleto de um lado para o outro dentro do alcance da patrulha."""
        if not self.is_dead:  # Se o esqueleto não estiver morto, patrulha
            if self.is_backstepping:
                # Se está em backstep, não faz a patrulha normal
                self.x -= self.direction * self.backstep_distance * dt
                if (time() - self.backstep_timer) > self.backstep_duration:
                    self.is_backstepping = False
            else:
                self.x += self.direction * self.speed * dt
                if self.x > self.start_x + self.patrol_range:
                    self.direction = -1
                    self.current_image = self.walking_animation_left
                elif self.x < self.start_x - self.patrol_range:
                    self.direction = 1
                    self.current_image = self.walking_animation_right
            # Atualiza as animações apenas se o esqueleto não estiver morto
            self.walking_animation_right.update()
            self.walking_animation_left.update()

    def update(self, dt, player):
        """Atualiza o estado do esqueleto."""
        if not self.is_dead:
            self.patrol(dt)
            distance_to_player = sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2)
            if distance_to_player < 10:  # Ataca se o jogador estiver próximo
                self.attack_player(player)
        else:
            self.walking_animation_right = None  # Para a animação
            self.walking_animation_left = None  # Para a animação

    def take_damage(self, damage, player):
        '''Som de dano ao monstro'''
        damage_skeleton = Sound("../efeitos_sonoros/damage_skeleton.mp3")
        damage_skeleton.play()

        """Aplica dano ao esqueleto e faz ele dar um backstep."""
        if not self.is_dead:
            self.health -= damage
            if self.health <= 0:
                self.die()
            else:
                self.is_backstepping = True
                self.backstep_timer = time()  # Marca o tempo de início do backstep

    def die(self):
        """Marca o esqueleto como morto e transforma sua imagem no osso."""
        self.is_dead = True
        # Desativa a animação e movimento, já que ele morreu
        self.walking_animation_right = None
        self.walking_animation_left = None


    def attack_player(self, player):
        """Ataca o jogador."""
        if not player.is_invincible:
            player.lose_life()

    def draw(self):
        """Desenha o esqueleto ou o osso, se estiver morto."""
        if not self.is_dead:
            self.current_image.x = self.x
            self.current_image.y = self.y
            self.current_image.draw()
class Vampire:
    def __init__(self, x, y):
        """Inicializa o vampiro."""
        self.x = x
        self.y = y
        self.width = 47
        self.height = 47
        self.walking_animation_right = Animation("../images/characters/vampire_right.png", 4)
        self.walking_animation_right.set_sequence(0, 3, loop=True)
        self.walking_animation_right.set_total_duration(1000)
        self.walking_animation_left = Animation("../images/characters/vampire_left.png", 4)
        self.walking_animation_left.set_sequence(0, 3, loop=True)
        self.walking_animation_left.set_total_duration(1000)
        self.current_image = self.walking_animation_right
        self.speed = 30
        self.health = 400
        self.is_dead = False
        self.attack_range = 10

        # Variáveis de controle de backstep
        self.is_backstepping = False
        self.backstep_duration = 0.3  # Duração do backstep (em segundos)
        self.backstep_distance = 50  # Distância do backstep (em pixels)
        self.backstep_timer = 0

    def move_towards_player(self, player, dt):
        """Move o vampiro na direção do jogador."""
        if not self.is_dead:
            if self.is_backstepping:
                # Se está em backstep, move na direção oposta ao movimento atual
                if self.current_image == self.walking_animation_left:
                    self.x += self.backstep_distance * dt  # Backstep para a direita
                else:
                    self.x -= self.backstep_distance * dt  # Backstep para a esquerda

                if (time() - self.backstep_timer) > self.backstep_duration:
                    self.is_backstepping = False
            else:
                # Movimentação normal para o jogador
                player_center_x = player.x + player.width / 2
                player_center_y = player.y + player.height / 2
                enemy_center_x = self.x + self.width / 2
                enemy_center_y = self.y + self.height / 2

                dx = player_center_x - enemy_center_x
                dy = player_center_y - enemy_center_y
                distance = sqrt((dx ** 2) + (dy ** 2))

                if distance < 1e-3:
                    return

                angle = atan2(dy, dx)
                direction_x = cos(angle)
                direction_y = sin(angle)

                self.x += direction_x * self.speed * dt
                self.y += direction_y * self.speed * dt

                if direction_x < 0:
                    self.current_image = self.walking_animation_left
                else:
                    self.current_image = self.walking_animation_right

                self.walking_animation_right.update()
                self.walking_animation_left.update()

                if distance < self.attack_range:
                    self.attack_player(player)

    def take_damage(self, damage, player):
        '''Som de dano ao vampiro'''
        damage_vampire = Sound("../efeitos_sonoros/damage_vampire.mp3")
        damage_vampire.play()
        """Aplica dano ao vampiro e faz ele dar um backstep."""
        if not self.is_dead:
            self.health -= damage
            if self.health <= 0:
                self.die()
            else:
                self.is_backstepping = True
                self.backstep_timer = time()  # Marca o tempo de início do backstep

    def die(self):
        """Marca o vampiro como morto."""
        self.is_dead = True

    def attack_player(self, player):
        """Ataca o jogador."""
        if not player.is_invincible:
            player.lose_life()

    def draw(self):
        """Desenha o vampiro."""
        if not self.is_dead:
            self.current_image.x = self.x
            self.current_image.y = self.y
            self.current_image.draw()

    def update(self, dt, player):
        """Atualiza o estado do vampiro."""
        if not self.is_dead:
            self.move_towards_player(player, dt)

class Skull:
    def __init__(self, x, y):
        """Inicializa o Skull."""
        self.x = x
        self.y = y
        self.width = 42
        self.height = 42
        self.walking_animation_right = Animation("../images/characters/skull_right.png", 4)
        self.walking_animation_right.set_sequence(0, 3, loop=True)
        self.walking_animation_right.set_total_duration(1000)
        self.walking_animation_left = Animation("../images/characters/skull_left.png", 4)
        self.walking_animation_left.set_sequence(0, 3, loop=True)
        self.walking_animation_left.set_total_duration(1000)
        self.current_image = self.walking_animation_right
        self.speed = 100
        self.max_speed = 150
        self.min_speed = 50
        self.acceleration = 200
        self.deceleration_factor = 0.1
        self.health = 200
        self.is_dead = False
        self.attack_range = 0
        self.detection_range = 2000
        self.oscillation_phase = 0
        self.previous_direction = (1, 0)

        # Variáveis de controle de backstep
        self.is_backstepping = False
        self.backstep_duration = 0.5  # Duração do backstep (em segundos)
        self.backstep_distance = 50  # Distância do backstep (em pixels)
        self.backstep_timer = 0

    def move_towards_player(self, player, dt):
        """Move o Skull na direção do jogador."""
        if not self.is_dead:
            if self.is_backstepping:
                # Se está em backstep, move na direção oposta ao movimento atual
                if self.current_image == self.walking_animation_left:
                    self.x += self.backstep_distance * dt  # Backstep para a direita
                else:
                    self.x -= self.backstep_distance * dt  # Backstep para a esquerda

                if (time() - self.backstep_timer) > self.backstep_duration:
                    self.is_backstepping = False
            else:
                # Movimentação normal para o jogador
                player_center_x = player.x + player.width / 2
                player_center_y = player.y + player.height / 2
                enemy_center_x = self.x + self.width / 2
                enemy_center_y = self.y + self.height / 2

                dx = player_center_x - enemy_center_x
                dy = player_center_y - enemy_center_y
                distance = sqrt(dx ** 2 + dy ** 2)

                if distance > self.detection_range:
                    return

                angle = atan2(dy, dx)
                direction_x = cos(angle)
                direction_y = sin(angle)

                previous_angle = atan2(self.previous_direction[1], self.previous_direction[0])
                angle_difference = abs(degrees(angle - previous_angle)) % 360
                if angle_difference > 90:
                    self.speed = max(self.speed * self.deceleration_factor, self.min_speed)

                self.previous_direction = (direction_x, direction_y)
                self.speed = min(self.speed + self.acceleration * dt, self.max_speed)

                self.oscillation_phase += 2 * pi * dt
                oscillation_angle = 0.4 * sin(self.oscillation_phase)
                direction_x = cos(angle + oscillation_angle)
                direction_y = sin(angle + oscillation_angle)

                self.x += direction_x * self.speed * dt
                self.y += direction_y * self.speed * dt

                if direction_x < 0:
                    self.current_image = self.walking_animation_left
                else:
                    self.current_image = self.walking_animation_right

                self.walking_animation_right.update()
                self.walking_animation_left.update()

                if distance < self.attack_range:
                    self.attack_player(player)

    def take_damage(self, damage, player):
        '''Som de dano ao Skull'''
        damage_skull = Sound("../efeitos_sonoros/damage_skull.mp3")
        damage_skull.play()
        """Aplica dano ao Skull e faz ele dar um backstep."""
        if not self.is_dead:
            self.health -= damage
            if self.health <= 0:
                self.die()
            else:
                self.is_backstepping = True
                self.backstep_timer = time()  # Marca o tempo de início do backstep

    def die(self):
        """Marca o Skull como morto."""
        self.is_dead = True

    def attack_player(self, player):
        """Ataca o jogador."""
        if not player.is_invincible:
            player.lose_life()

    def draw(self):
        """Desenha o Skull."""
        if not self.is_dead:
            self.current_image.x = self.x
            self.current_image.y = self.y
            self.current_image.draw()

    def update(self, dt, player):
        """Atualiza o estado do Skull."""
        if not self.is_dead:
            self.move_towards_player(player, dt)
