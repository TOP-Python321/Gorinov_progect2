from pathlib import Path
from sys import path


ROOT_DIR = Path(path[0]).parent.parent.parent

# путь к файлу с сохранением данных питамца
creature_save = ROOT_DIR / 'data/creature.save'

# соотношение игрового дня к часам реального времени. При расчете параметров питомца после повторного запуска приложения
days_hours = (1, 2)

# один игровой день равен 720000 милисекунд (2 часа игры == 1 мин. реального времени).
game_hours: int = 30000

# имя питомца по умолчанию (пока не реализован запрос имени)
default_name = 'Питомец'


# пути к картинкам проекта
IMAGES_PATH = {
    'cat': {
        'main': ROOT_DIR / 'data/images/cat.png',
        'feed': ROOT_DIR / 'data/images/btn1.png',
        'water': ROOT_DIR / 'data/images/water.png',
        'pet': ROOT_DIR / 'data/images/pet_cat.png',
        'play_pet': ROOT_DIR / 'data/images/btn2.png',
        'play_rope': ROOT_DIR / 'data/images/cat_play_rope.png',
        'miss': ROOT_DIR / 'data/images/cat_miss.png',
        'sleep': ROOT_DIR / 'data/images/cat_sleep.png'
    },
    'dog': {
        'main': ROOT_DIR / 'data/images/dog.png',
        'feed': ROOT_DIR / 'data/images/btn1.png',
        'water': ROOT_DIR / 'data/images/water.png',
        'pet': ROOT_DIR / 'data/images/pet_dog.png',
        'play_pet': ROOT_DIR / 'data/images/btn2.png',
        'run': ROOT_DIR / 'data/images/dog_run.png',
        'miss': ROOT_DIR / 'data/images/dog_miss.png',
        'sleep': ROOT_DIR / 'data/images/dog_sleep.png'
    },
    'no_action': ROOT_DIR / 'data/images/no_action.png'
}
