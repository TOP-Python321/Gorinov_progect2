from src.tamagotchi.model import *
from data.data import *
from pathlib import Path
from sys import path

ROOT_DIR = Path(path[0]).parent.parent.parent

cat_kind = Kind(
    'Кот',
    IMAGES_PATH['cat']['main'],
    {
        Maturity.CUB: MatureOptions(
            4,
            Health(10, 0, 20),
            Thirst(5, 0, 25),
            Satiety(5, 0, 25),
            Mood(10, 0, 50),
            player_actions=[
                Feed(amount=20, image=IMAGES_PATH['cat']['feed']),
                Water(image=IMAGES_PATH['cat']['water']),
                Pet(image=IMAGES_PATH['cat']['pet']),
                PlayPet(image=IMAGES_PATH['cat']['play_pet'])
            ],
            creature_action={
                PlayRope(timer=100, image=IMAGES_PATH['cat']['play_rope']),
                Miss(timer=80, image=IMAGES_PATH['cat']['miss']),
                Sleep(timer=220, image=IMAGES_PATH['cat']['sleep']),
            }
        ),
        Maturity.YOUNG: MatureOptions(
            10,
            Health(0, 0, 50),
            Thirst(0, 0, 30),
            Satiety(0, 0, 30),
            Mood(0, 0, 50),
            player_actions=[
                Feed(amount=25, image=IMAGES_PATH['cat']['feed']),
                Water(image=IMAGES_PATH['cat']['water']),
                Pet(image=IMAGES_PATH['cat']['pet']),
                PlayPet(image=IMAGES_PATH['cat']['play_pet'])
            ],
            creature_action={
                PlayRope(timer=100, image=IMAGES_PATH['cat']['play_rope']),
                Miss(timer=80, image=IMAGES_PATH['cat']['miss']),
                Sleep(timer=120, image=IMAGES_PATH['cat']['sleep']),
            }
        ),
        Maturity.ADULT: MatureOptions(
            20,
            Health(0, 0, 45),
            Thirst(0, 0, 25),
            Satiety(0, 0, 25),
            Mood(0, 0, 40),
            player_actions=[
                Feed(amount=20, image=IMAGES_PATH['cat']['feed']),
                Water(image=IMAGES_PATH['cat']['water']),
                Pet(image=IMAGES_PATH['cat']['pet']),
                PlayPet(image=IMAGES_PATH['cat']['play_pet'])
            ],
            creature_action={
                PlayRope(timer=180, image=IMAGES_PATH['cat']['play_rope']),
                Miss(timer=120, image=IMAGES_PATH['cat']['miss']),
                Sleep(timer=60, image=IMAGES_PATH['cat']['sleep']),
            }
        ),
        Maturity.OLD: MatureOptions(
            25,
            Health(0, 0, 35),
            Thirst(0, 0, 20),
            Satiety(0, 0, 20),
            Mood(0, 0, 30),
            player_actions=[
                Feed(amount=10, image=IMAGES_PATH['cat']['feed']),
                Water(image=IMAGES_PATH['cat']['water']),
                Pet(image=IMAGES_PATH['cat']['pet']),
                PlayPet(image=IMAGES_PATH['cat']['play_pet'])
            ],
            creature_action={
                Miss(timer=60, image=IMAGES_PATH['cat']['miss']),
                Sleep(timer=180, image=IMAGES_PATH['cat']['sleep']),
            }
        ),
    }
)

dog_kind = Kind(
    'Пёс',
    IMAGES_PATH['dog']['main'],
    {
        Maturity.CUB: MatureOptions(
            3,
            Health(15, 0, 25),
            Thirst(3, 0, 20),
            Satiety(3, 0, 20),
            Mood(10, 0, 40),
            player_actions=[
                Feed(amount=20, image=IMAGES_PATH['dog']['feed']),
                Water(image=IMAGES_PATH['dog']['water']),
                Pet(image=IMAGES_PATH['dog']['pet']),
                PlayPet(image=IMAGES_PATH['dog']['play_pet'])
            ],
            creature_action={
                Run(timer=100, image=IMAGES_PATH['dog']['run']),
                Miss(timer=80, image=IMAGES_PATH['dog']['miss']),
                Sleep(timer=220, image=IMAGES_PATH['dog']['sleep']),
            }
        ),
        Maturity.YOUNG: MatureOptions(
            9,
            Health(0, 0, 50),
            Thirst(0, 0, 35),
            Satiety(0, 0, 40),
            Mood(0, 0, 50),
            player_actions=[
                Feed(amount=35, image=IMAGES_PATH['dog']['feed']),
                Water(image=IMAGES_PATH['dog']['water']),
                Pet(image=IMAGES_PATH['dog']['pet']),
                PlayPet(image=IMAGES_PATH['dog']['play_pet'])
            ],
            creature_action={
                Run(timer=100, image=IMAGES_PATH['dog']['run']),
                Miss(timer=80, image=IMAGES_PATH['dog']['miss']),
                Sleep(timer=120, image=IMAGES_PATH['dog']['sleep']),
            }
        ),
        Maturity.ADULT: MatureOptions(
            15,
            Health(0, 0, 45),
            Thirst(0, 0, 35),
            Satiety(0, 0, 35),
            Mood(0, 0, 45),
            player_actions=[
                Feed(amount=25, image=IMAGES_PATH['dog']['feed']),
                Water(image=IMAGES_PATH['dog']['water']),
                Pet(image=IMAGES_PATH['dog']['pet']),
                PlayPet(image=IMAGES_PATH['dog']['play_pet'])
            ],
            creature_action={
                Run(timer=180, image=IMAGES_PATH['dog']['run']),
                Miss(timer=120, image=IMAGES_PATH['dog']['miss']),
                Sleep(timer=60, image=IMAGES_PATH['dog']['sleep']),
            }
        ),
        Maturity.OLD: MatureOptions(
            20,
            Health(0, 0, 35),
            Thirst(0, 0, 30),
            Satiety(0, 0, 30),
            Mood(0, 0, 30),
            player_actions=[
                Feed(amount=20, image=IMAGES_PATH['dog']['feed']),
                Water(image=IMAGES_PATH['dog']['water']),
                Pet(image=IMAGES_PATH['dog']['pet']),
                PlayPet(image=IMAGES_PATH['dog']['play_pet'])
            ],
            creature_action={
                Miss(timer=60, image=IMAGES_PATH['dog']['miss']),
                Sleep(timer=180, image=IMAGES_PATH['dog']['sleep'])
            }
        ),
    }
)