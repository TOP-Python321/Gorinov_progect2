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

sem = Creature(Kind.CAT, 'Сэм')
for elem in sem.creature_action:
    print(elem, elem.__class__)

print(f'{[elem.__class__.__name__ for elem in sem.creature_action] = }')

sem._grow_up()

print(sem.mature)

# Тесты Thirst и Water
sem.params[Thirst].value += 20


def print_sem_params():
    print(*[f'{sem.params[k].__class__.__name__} = {sem.params[k].value}' for k in sem.params.keys()], sep='\n', end='\n\n')


print_sem_params()
print(f'sem.update()'f'{sem.update()}')
print_sem_params()
print(f'sem.update()'f'{sem.update()}')
print_sem_params()

print(f'sem.player_actions[{sem.player_actions[1].__class__.__name__}].action()')
sem.player_actions[1].action()
print_sem_params()

# Тест Mood
print(f'sem.creature_action = {[elem.__class__.__name__ for elem in sem.creature_action]}')
for elem in sem.creature_action:
    elem.action()
print_sem_params()