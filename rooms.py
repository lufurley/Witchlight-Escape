from random import randint
from enemies import Skeleton, Vampire, Skull
from PPlay.gameimage import *
from PIL import Image
from objects import Key
from boss import Wizard

class RoomLibrary:
    def __init__(self):
        self.rooms = {
            1: {
                'background': GameImage("../images/rooms/room1.png"),
                'mask': Image.open("../images/rooms/path1.png").convert("L"),
                'left': None, 'right': 2, 'up': None, 'down': None,
            },
            2: {
                'background': GameImage("../images/rooms/room2.png"),
                'mask': Image.open("../images/rooms/path2.png").convert("L"),
                'left': 1, 'right': None, 'up': 3, 'down': 6,
                'skeleton_positions': [(700, 200), (700, 400), (700, 600)],
            },
            3: {
                'background': GameImage("../images/rooms/room3.png"),
                'mask': Image.open("../images/rooms/path3.png").convert("L"),
                'left': None, 'right': 4, 'up': None, 'down': 2,
                'skeleton_positions': [(700, 400)],
                'skull_positions': [(200, 400), (600, 400)]
            },
            4: {
                'background': GameImage("../images/rooms/room4.png"),
                'mask': Image.open("../images/rooms/path4.png").convert("L"),
                'left': 3, 'right': None, 'up': None, 'down': 5,
                'vampire_positions': [(500, 600), (700, 600)],
                'skeleton_positions': [(500, 300), (500, 400)],
            },
            5: {
                'background': GameImage("../images/rooms/room5.png"),
                'mask': Image.open("../images/rooms/path5.png").convert("L"),
                'left': None, 'right': None, 'up': 4, 'down': None,
                'skull_positions': [(500, 650), (700, 650)],
                'skeleton_positions': [(600, 350), (600, 550)],
                'key_position': (630, 450),
            },
            6: {
                'background': GameImage("../images/rooms/room6.png"),
                'mask': Image.open("../images/rooms/path6.png").convert("L"),
                'left': None, 'right': 7, 'up': 2, 'down': None,
                'skeleton_positions': [(400, 300), (400, 500), (700, 300), (700, 500)],
                'skull_positions': [(500, 400)],
            },
            7: {
                'background': GameImage("../images/rooms/room7.png"),
                'mask': Image.open("../images/rooms/path7.png").convert("L"),
                'left': 6, 'right': 9, 'up': None, 'down': 8,
                'vampire_positions': [(400, 500), (700, 500)],
                'skull_positions': [(550, 500)],
            },
            8: {
                'background': GameImage("../images/rooms/room8.png"),
                'mask': Image.open("../images/rooms/path8.png").convert("L"),
                'left': None, 'right': None, 'up': 7, 'down': None,
                'vampire_positions': [(600, 400), (600, 600)],
                'skeleton_positions': [(450, 300), (450, 500), (650, 300), (650, 500)],
            },
            9: {
                'background': GameImage("../images/rooms/room9.png"),
                'mask': Image.open("../images/rooms/path9.png").convert("L"),
                'left': 7, 'right': 10, 'up': None, 'down': None,
                'skeleton_positions': [(300, 700), (800, 700), (300, 400), (800, 400)],
                'skull_positions': [(600, 300), (600, 700)],
            },
            10: {
                'background': GameImage("../images/rooms/room10.png"),
                'mask': Image.open("../images/rooms/path10.png").convert("L"),
                'left': 9, 'right': None, 'up': 11, 'down': 12,
                'skeleton_positions': [(600, 650), (600, 450), (600, 250)],
                'skull_positions': [(600, 300), (600, 700)],
            },
            11: {
                'background': GameImage("../images/rooms/room11.png"),
                'mask': Image.open("../images/rooms/path11.png").convert("L"),
                'left': None, 'right': None, 'up': None, 'down': 10,
                'vampire_positions': [(400, 300), (750, 300)],
                'skull_positions': [(575, 300)],
            },
            12: {
                'background': GameImage("../images/rooms/room12.png"),
                'mask': Image.open("../images/rooms/path12.png").convert("L"),
                'left': None, 'right': None, 'up': 10, 'down': None,
                'wizard_positions': [(500, 500)],
            },
        }

        # Status inicial das salas (False significa que os inimigos ainda estão presentes)
        self.room_status = {room_id: False for room_id in self.rooms.keys()}

    def get_room(self, current_room):
        """Retorna os dados da sala especificada pelo ID."""
        room = self.rooms.get(current_room, None)
        if room and 'key_position' in room:
            # Cria a chave na posição especificada
            key_position = room['key_position']
            key = Key(key_position[0], key_position[1])  # Classe Key definida
            room['key'] = key  # Adiciona a chave à sala
        return room

    def mark_room_complete(self, room_id):
        """Marca uma sala como concluída (inimigos não reaparecerão)."""
        self.room_status[room_id] = True

    def spawn_enemies(self, room_id):
        """Gera inimigos na sala especificada."""
        room = self.get_room(room_id)
        if not room or self.room_status[room_id]:
            # Se a sala não existir ou já estiver concluída, retorna listas vazias
            return [], [], [], []

        vampires = []
        skeletons = []
        skulls = []
        wizards = []

        # Verifica inimigos na sala
        if 'vampire_positions' in room:
            vampires.extend([Vampire(x, y) for x, y in room['vampire_positions']])

        if 'skeleton_positions' in room:
            skeletons.extend([Skeleton(x, y) for x, y in room['skeleton_positions']])

        if 'skull_positions' in room:
            skulls.extend([Skull(x, y) for x, y in room['skull_positions']])

        if 'wizard_positions' in room:
            wizards.extend([Wizard(x, y) for x, y in room['wizard_positions']])

        return vampires, skeletons, skulls, wizards
