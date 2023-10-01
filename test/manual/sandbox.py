"""
Пространство имён для ручных тестов.

python -i sandbox.py
"""

from pathlib import Path
from sys import path

ROOT_DIR = Path(path[0]).parent.parent
print(ROOT_DIR)
path.insert(0, str(ROOT_DIR / 'src/tamagotchi'))
print(path[0])

from model import *

sem = Creature(Kind.CAT, 'Сем')
for elem in sem.creature_action:
    print(elem, elem.__class__)

print(sem.creature_action)
sem._grow_up()

print(sem.creature_action)
print(sem.mature)
