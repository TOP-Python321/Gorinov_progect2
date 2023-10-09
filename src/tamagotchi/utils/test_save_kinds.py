from sys import path
from pathlib import Path
from json import dumps as jdumps, loads as jloads

from src.tamagotchi.model import *

test_kinds = {
    'Кот': {
        'image': 'data/images/cat.png',
        'Maturity': {
            'CUB': {
                'Health': (10, 0, 20),
                'Thirst': (5, 0, 25),
                'Satiety': (5, 0, 25),
                'Mood': (10, 0, 50),
                'player_actions': [
                    ('Feed', 20),
                    ('Water', 0),
                    ('Pet', 0),
                    ('PlayPet', 0)
                ],
                'creature_action': [
                    ('PlayRope', 100),
                    ('Miss', 80)
                ]
            }
        }
    }
}
kinds_path = Path(path[0]).parent.parent.parent / 'data/kinds.save'
data = jdumps(test_kinds, ensure_ascii=False)
kinds_path.write_text(data, encoding='utf-8')

test_read = kinds_path.read_text(encoding='utf-8')
