from pathlib import Path
from sys import path
from pytest import fixture
from random import randrange as rr

path.append(str(Path(path[0]).parent.parent / 'src/tamagotchi'))
print(path)

from model import *

# @fixture
# def health():
    # return Health(rr(0, 10), rr(0, 10), rr(0, 10))
    
def test_health():
    health = Health(15, 10, 20)
    assert health.min < health.value