from src.tamagotchi.model import *
from pathlib import Path
from sys import path

ROOT_DIR = Path(path[0]).parent.parent.parent

cat_kind = Kind(
    'Кот',
    ROOT_DIR / 'data/images/cat.png',
    {
        Maturity.CUB: MatureOptions(
            4,
            Health(10, 0, 20),
            Thirst(5, 0, 25),
            Satiety(5, 0, 25),
            Mood(10, 0, 50),
            player_actions=[
                Feed(amount=20, image=ROOT_DIR / 'data/images/btn1.png'),
                Water(image=ROOT_DIR / 'data/images/water.png'),
                Pet(image=ROOT_DIR / 'data/images/pet_cat.png'),
                PlayPet(image=ROOT_DIR / 'data/images/btn2.png')
            ],
            creature_action={
                PlayRope(timer=100, image=ROOT_DIR / 'data/images/cat_sleep.png'),
                Miss(timer=80, image=ROOT_DIR / 'data/images/cat_peet.png')
            }
        ),
        Maturity.YOUNG: MatureOptions(
            10,
            Health(0, 0, 50),
            Thirst(0, 0, 30),
            Satiety(0, 0, 30),
            Mood(0, 0, 50),
            player_actions=[
                Feed(amount=25, image=ROOT_DIR / 'data/images/btn1.png'),
                Water(image=ROOT_DIR / 'data/images/btn1.png'),
                Pet(image=ROOT_DIR / 'data/images/btn1.png'),
                PlayPet(image=ROOT_DIR / 'data/images/btn1.png')
            ],
            creature_action={
                PlayRope(timer=100, image=ROOT_DIR / 'data/images/cat_sleep.png'),
                Miss(timer=80, image=ROOT_DIR / 'data/images/cat_peet.png'),
                Sleep(timer=120, image=ROOT_DIR / 'data/images/cat_sleep.png'),
            }
        ),
        Maturity.ADULT: MatureOptions(
            20,
            Health(0, 0, 45),
            Thirst(0, 0, 25),
            Satiety(0, 0, 25),
            Mood(0, 0, 40),
            player_actions=[
                Feed(amount=20, image=ROOT_DIR / 'data/images/btn1.png'),
                Water(image=ROOT_DIR / 'data/images/btn1.png'),
                Pet(image=ROOT_DIR / 'data/images/btn1.png'),
                PlayPet(image=ROOT_DIR / 'data/images/btn1.png')
            ],
            creature_action={
                PlayRope(timer=180),
                Miss(timer=120),
                Sleep(timer=60),
            }
        ),
        Maturity.OLD: MatureOptions(
            12,
            Health(0, 0, 35),
            Thirst(0, 0, 20),
            Satiety(0, 0, 20),
            Mood(0, 0, 30),
            player_actions=[
                Feed(amount=10, image=ROOT_DIR / 'data/images/btn1.png'),
                Water(image=ROOT_DIR / 'data/images/btn1.png'),
                Pet(image=ROOT_DIR / 'data/images/btn1.png'),
                PlayPet(image=ROOT_DIR / 'data/images/btn1.png')
            ],
            creature_action={
                Miss(timer=80),
                Sleep(timer=30)
            }
        ),
    }
)

dog_kind = Kind(
    'Пёс',
    ROOT_DIR / 'data/images/dog.png',
    {
        Maturity.CUB: MatureOptions(
            4,
            Health(12, 0, 25),
            Satiety(7, 0, 25),
            player_actions=[
                Feed(amount=20, image=ROOT_DIR / 'data/images/btn1.png'),
            ],
            creature_action={
                Miss(timer=100),
            }
        ),
        Maturity.YOUNG: MatureOptions(
            11,
            Health(0, 0, 50),
            Satiety(0, 0, 30),
            player_actions=[
                Feed(amount=25, image=ROOT_DIR / 'data/images/btn1.png'),
            ],
            creature_action={
                Miss(timer=100),
                Sleep(timer=120),
            }
        ),
        Maturity.ADULT: MatureOptions(
            20,
            Health(0, 0, 45),
            Satiety(0, 0, 25),
            player_actions=[
                Feed(amount=20, image=ROOT_DIR / 'data/images/btn1.png'),
            ],
            creature_action={
                Sleep(timer=60),
                Miss(timer=180),
            }
        ),
        Maturity.OLD: MatureOptions(
            12,
            Health(0, 0, 35),
            Satiety(0, 0, 20),
            player_actions=[
                Feed(amount=10, image=ROOT_DIR / 'data/images/btn1.png'),
            ],
            creature_action={
                Sleep(timer=30)
            }
        ),
    }
)