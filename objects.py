from PPlay.animation import Animation
from PPlay.sound import *

class Key:
    def __init__(self, x, y):
        """Inicializa a chave com sua posição, tamanho e animação."""
        self.x = x
        self.y = y
        self.width = 40  # Largura da chave
        self.height = 40  # Altura da chave
        self.image = Animation("../images/objects/key.png", 4)  # Carrega a animação da chave
        self.image.set_sequence(0, 3, loop=True)  # Configura os quadros para looping contínuo
        self.image.set_total_duration(1000)  # Define a duração total da animação
        self.is_collected = False  # Estado inicial: chave não coletada

    def draw(self):
        """Desenha a chave na tela se ela ainda não foi coletada."""
        if not self.is_collected:
            self.image.x = self.x  # Atualiza a posição x da animação
            self.image.y = self.y  # Atualiza a posição y da animação
            self.image.update()  # Atualiza os quadros da animação
            self.image.draw()  # Renderiza a animação na tela

    def update(self):
        """Atualiza a lógica da chave (pode ser expandido conforme necessário)."""
        pass

    def collect(self, player):
        """Verifica se o jogador coletou a chave e atualiza o estado."""
        if not self.is_collected:
            # Define as caixas de colisão do jogador e da chave
            player_box = {
                "x": player.x,
                "y": player.y,
                "width": player.width,
                "height": player.height,
            }
            key_box = {
                "x": self.x,
                "y": self.y,
                "width": self.width,
                "height": self.height,
            }

            # Verifica colisão entre o jogador e a chave
            if (
                player_box["x"] < key_box["x"] + key_box["width"]
                and player_box["x"] + player_box["width"] > key_box["x"]
                and player_box["y"] < key_box["y"] + key_box["height"]
                and player_box["y"] + player_box["height"] > key_box["y"]
            ):
                pickup_key = Sound("../efeitos_sonoros/pick-up-key.mp3")
                pickup_key.play()
                self.is_collected = True  # Marca a chave como coletada
                player.has_key = True  # Atualiza o estado do jogador para "possui chave"

