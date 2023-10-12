# from src.tamagotchi.model import *

from sys import path
from pathlib import Path
from json import dumps as jdumps, loads as jloads

ROOT_DIR = Path(path[0]).parent.parent

test_kinds = {
    'Кот': {
        'image': 'data/images/cat.png',
        'Maturity': {
            'CUB': {
                'params': {
                    'Health': (10, 0, 20),
                    'Thirst': (5, 0, 25),
                    'Satiety': (5, 0, 25),
                    'Mood': (10, 0, 50),
                },
                'player_actions': [
                    ('Feed', ('amount', 20), ('image', 'data/images/btn1.png')),
                    ('Water', ('image', 'data/images/btn1.png')),
                    ('Pet', ('image', 'data/images/btn1.png')),
                    ('PlayPet', ('image', 'data/images/btn1.png'))
                ],
                'creature_action': [
                    ('PlayRope', ('timer', 100)),
                    ('Miss', ('timer', 80))
                ]
            }
        }
    }
}
kinds_path = Path(path[0]).parent.parent.parent / 'data/kinds.save'
data = jdumps(test_kinds, ensure_ascii=False)
kinds_path.write_text(data, encoding='utf-8')

test_read = kinds_path.read_text(encoding='utf-8')
